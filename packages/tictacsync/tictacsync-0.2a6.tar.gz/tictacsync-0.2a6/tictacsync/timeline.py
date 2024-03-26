# -*- coding: utf-8 -*-
import numpy, tempfile, copy
# import ffmpeg, pathlib, os
import ffmpeg
from loguru import logger
import sox
from pathlib import Path
from rich import print
from itertools import groupby
# import opentimelineio as otio
from datetime import timedelta
import pprint, shutil, os

from inspect import currentframe, getframeinfo
try:
    from . import yaltc
except:
    import yaltc

CLUSTER_GAP = 0.5 # secs between multicam clusters
DEL_TEMP = False
OUT_DIR_DEFAULT = 'SyncedMedia'

# utility for accessing pathnames
def _pathname(tempfile_or_path) -> str:
    if isinstance(tempfile_or_path, str):
        return tempfile_or_path
    if isinstance(tempfile_or_path, yaltc.Recording):
        return str(tempfile_or_path.AVpath)
    if isinstance(tempfile_or_path, Path):
        return str(tempfile_or_path)
    if isinstance(tempfile_or_path, tempfile._TemporaryFileWrapper):
        return tempfile_or_path.name
    else:
        raise Exception('%s should be Path or tempfile...'%tempfile_or_path)

# utility for printing groupby results
def print_grby(grby):
    for key, keylist in grby:
        print('\ngrouped by %s:'%key)
        for e in keylist:
            print(' ', e)

# deltatime utility
def from_midnight(a_datetime) -> timedelta:
    # returns a deltatime from a datetime, "dropping" the date information
    return(timedelta(hours=a_datetime.hour, minutes=a_datetime.minute,
                     seconds=a_datetime.second,
                     microseconds=a_datetime.microsecond))

# utility for extracting one audio channel
def _extr_channel(source, dest, channel):
    # int channel = 1 for first channel
    # returns nothing, output is written to the filesystem
    sox_transform = sox.Transformer()
    mix_dict = {1:[channel]}
    logger.debug('sox args %s %s %s'%(source, dest, mix_dict))    
    sox_transform.remix(mix_dict)
    logger.debug('sox transform %s'%str(sox_transform))
    status = sox_transform.build(str(source), str(dest))
    logger.debug('sox status %s'%status)

def _split_channels(multi_chan_audio:Path) -> list:
    nchan = sox.file_info.channels(_pathname(multi_chan_audio))
    source = _pathname(multi_chan_audio)
    paths = []
    for i in range(nchan):
        out_fh = tempfile.NamedTemporaryFile(suffix='.wav',
                delete=DEL_TEMP)
        sox_transform = sox.Transformer()
        mix_dict = {1:[i+1]}
        sox_transform.remix(mix_dict)
        dest = _pathname(out_fh)
        status = sox_transform.build(source, dest)
        logger.debug('source %s dest %s'%(source, dest))
        logger.debug('sox status %s'%status)
        paths.append(out_fh)
    logger.debug('paths %s'%paths)
    return paths


def _sox_combine(paths) -> Path:
    """
    Combines files referred by the list of Path into a new temporary files
    passed on return each files are stacked in a different channel, so 
    len(paths) == n_channels
    """
    if len(paths) == 1: # one device only, nothing to stack
        logger.debug('one device only, nothing to stack')
        return paths[0]
    out_file_handle = tempfile.NamedTemporaryFile(suffix='.wav',
        delete=DEL_TEMP)
    filenames = [_pathname(p) for p in paths]
    out_file_name = _pathname(out_file_handle)
    logger.debug('combining files: %s into %s'%(
        filenames,
        out_file_name))
    cbn = sox.Combiner()
    cbn.set_input_format(file_type=['wav']*len(paths))
    status = cbn.build(
        filenames,
        out_file_name,
        combine_type='merge')
    logger.debug('sox.build status: %s'%status)
    if status != True:
        print('Error, sox did not merge files in _sox_combine()')
        sys.exit(1)
    merged_duration = sox.file_info.duration(
        _pathname(out_file_handle))
    nchan = sox.file_info.channels(
        _pathname(out_file_handle)) 
    logger.debug('merged file duration %f s with %i channels '%
        (merged_duration, nchan))
    return out_file_handle

def _sox_mix(paths:list) -> tempfile.NamedTemporaryFile:
    """
    mix files referred by the list of Path into a new temporary files passed on return
    """
    cbn = sox.Combiner()
    N = len(paths)
    if N == 1: # nothing to mix
        return paths[0]
    cbn.set_input_format(file_type=['wav']*N)
    filenames = [_pathname(p) for p in paths]
    logger.debug('files to mix %s'%filenames)
    mixed_tempf = tempfile.NamedTemporaryFile(suffix='.wav',delete=DEL_TEMP)
    status = cbn.build(filenames,
                _pathname(mixed_tempf),
                combine_type='mix',
                input_volumes=[1/N]*N)
    logger.debug('sox.build status for mix: %s'%status)
    if status != True:
        print('Error, sox did not mix files in _sox_mix()')
        sys.exit(1)
    normed_tempfile = tempfile.NamedTemporaryFile(suffix='.wav',delete=DEL_TEMP)
    tfm = sox.Transformer()
    tfm.norm(-6)
    status = tfm.build(_pathname(mixed_tempf),_pathname(normed_tempfile))
    logger.debug('sox.build status for norm(): %s'%status)
    if status != True:
        print('Error, sox did not normalize file in _sox_mix()')
        sys.exit(1)
    return normed_tempfile


class AudioStitcherVideoMerger:
    """
    Typically each found video is associated with an AudioStitcherVideoMerger
    instance. AudioStitcherVideoMerger does the actual audio-video file
    processing of merging self.ref_recording (gen. a video) with all audio
    files in  self.edited_audio as determined by the Matcher
    object (it instanciates and manages AudioStitcherVideoMerger objects).

    All audio file edits are done using pysox and video+audio merging with
    ffmpeg. When necessary, clock drift is corrected for all overlapping audio
    devices to match the precise clock value of the ref recording (to a few
    ppm), using sox tempo transform.

    N.B.: A audio_stitch doesn't extend beyond the corresponding ref_recording
    video start and end times: it is not a audio montage for the whole movie
    project.


    Attributes:

        ref_recording : a Recording instance
            The video (or designated main sound) audio files are synced to

        edited_audio : dict as {Recording : path}
            keys are elements of matched_audio_recordings of class Recording
            and the value stores the Pathlib path of the eventual edited
            audio (trimmed , padded or time stretched). Before building the
            audio_montage, path points to the initial
            Recording.valid_sound

        synced_clip_dir : Path
            where synced clips are written

    """

    def __init__(self, reference_recording):
        self.ref_recording = reference_recording
        # self.matched_audio_recordings = []
        self.edited_audio = {}
        logger.debug('instantiating AudioStitcherVideoMerger for %s'%
                            reference_recording)

    def add_matched_audio(self, audio_rec):
        """
        Populates self.edited_audio, a dict as {Recording : path}

        AudioStitcherVideoMerger.add_matched_audio() is called
        within Matcher.scan_audio_for_each_ref_rec()

        Returns nothing, fills self.edited_audio dict with
        matched audio.

        """
        self.edited_audio[audio_rec] = audio_rec.valid_sound
        """
        Here at this point, self.edited_audio[audio_rec] is unedited but
        after a call to _edit_audio_file(), edited_audio[audio_rec] points to
        a new file and the precedent is unchanged (that's why from
        AudioStitcherVideoMerger instance to another
        audio_rec.valid_sound doesn't need to be reinitialized since
        it stays unchanged)
        """
        return

    def get_matched_audio_recs(self):
        """
        Returns audio recordings that overlap self.ref_recording.
        Simply keys of self.edited_audio dict
        """
        return list(self.edited_audio.keys())

    def _get_audio_devices(self):
        # ex {'RCR_A', 'RCR_B', 'RCR_C'} if multisound
        return set([r.device for r in self.get_matched_audio_recs()])

    def _get_all_recordings_for(self, device):
        # return recordings for a particular device, sorted by time
        recs = [a for a in self.get_matched_audio_recs() if a.device == device]
        recs.sort(key=lambda r: r.start_time)
        return recs

    def _dedrift_rec(self, rec):
        # first_audio_p = rec.AVpath
        initial_duration = sox.file_info.duration(
            _pathname(rec.valid_sound))
        sox_transform = sox.Transformer()
        # tempo_scale_factor = rec.device_relative_speed
        tempo_scale_factor = rec.device_relative_speed
        reC_dev = rec.device.name
        reF_dev = self.ref_recording.device.name
        if tempo_scale_factor > 1:
            print('[gold1]%s[/gold1] clock too fast relative to [gold1]%s[/gold1] so file is too long by a %f factor\n'%
                (reC_dev, reF_dev, tempo_scale_factor))
        else:
            print('[gold1]%s[/gold1] clock too slow relative to [gold1]%s[/gold1] so file is too short by a %f factor\n'%
                (reC_dev, reF_dev, tempo_scale_factor))
        sox_transform.tempo(tempo_scale_factor)
        # scaled_file = self._get_soxed_file(rec, sox_transform)
        logger.debug('sox_transform %s'%sox_transform.effects)
        self._edit_audio_file(rec, sox_transform)
        scaled_file_name = _pathname(self.edited_audio[rec])
        new_duration = sox.file_info.duration(scaled_file_name)
        # goal_duration = rec.get_corrected_duration()
        logger.debug('initial_duration %f new_duration %f ratio:%f'%(
            initial_duration, new_duration, initial_duration/new_duration))

    def _get_concatenated_audiofile_for(self, device):
        """
        return a handle for the final audio file formed by all detected
        overlapping recordings, produced by the same specified device.
        
        """
        logger.debug('concatenating device %s'%str(device))
        recordings = self._get_all_recordings_for(device)
        # [TODO here] Check if all unidentified device files are not
        # overlapping because they are considered produced by the same
        # device. If some overlap then necessarily they're from different
        # ones. List the files and warn the user there is a risk of error if
        # they're not from the same device.

        logger.debug('%i audio files for reference rec %s:'%(len(recordings),
            self.ref_recording))
        for r in recordings:
            logger.debug('  %s'%r)
        speeds = numpy.array([rec.get_speed_ratio(self.ref_recording)
                                    for rec in recordings])
        mean_speed = numpy.mean(speeds)
        for r in recordings:
            r.device_relative_speed = mean_speed
            # r.device_relative_speed = 0.9
            logger.debug('set device_relative_speed for %s'%r)
            logger.debug(' value: %f'%r.device_relative_speed)
            r.set_time_position_to(self.ref_recording)
            logger.debug('time_position for %s: %fs relative to %s'%(r,
                r.time_position, self.ref_recording))
        # st_dev_speeds just to check for anomalous situation
        st_dev_speeds = numpy.std(speeds)
        logger.debug('mean speed for %s: %.6f std dev: %.0e'%(device,
                                                    mean_speed,
                                                    st_dev_speeds))
        if st_dev_speeds > 1.0e-5:
            logger.error('too much variation for device speeds')
            sys.exit(1)
        """        
        Because of length
        transformations with pysox.tempo, it is not the sum of REC durations
        
                ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
                ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ref
                  ┏━━━━┓   ┏━━━━┓
                ┣━┻━━━━┻━━━┻━━━━┛ growing_file
        
                ├───────────────┤
                             end_time
        
        """

        # process first element 'by hand' outside the loop
        # first_audio is a Recording, not a path nor filehandle
        first_audio = recordings[0]
        needs_dedrift, delta = first_audio.needs_dedrifting()
        logger.debug('first audio is %s'%first_audio)
        logger.debug('checking drift, first audio: delta of %0.2f ms'%(
            delta*1e3))
        if needs_dedrift:
            self._dedrift_rec(first_audio)
        else:
            logger.debug('no time stretch for 1st audio')        
        self._pad_or_trim_first_audio(first_audio)
        # loop for the other files
        # growing_file = first_audio.edited_version
        growing_file = self.edited_audio[first_audio]
        for i, rec in enumerate(recordings[1:]):
            logger.debug('Padding and joining for %s'%rec)
            needs_dedrift, delta = rec.needs_dedrifting()
            logger.debug('next audio is %s'%rec)
            logger.debug('checking drift for next audio, delta of %0.2f ms'%(
                delta*1e3))
            if needs_dedrift:
                # logger.debug('dedrifting too...delta of %0.2f ms'%(delta*1e3))
                self._dedrift_rec(rec)
            else:
                logger.debug('no dedrifting')        
            end_time = sox.file_info.duration(growing_file.name)
            logger.debug('  growing_file %s'%(growing_file.name))
            logger.debug('  growing_file duration %.2f'%(end_time))
            logger.debug('  rec.time_position  for next audio %s %.2f'%(rec,
                rec.time_position))
            # TODO check if rec.needs_dedrifting() before padding
            pad_duration = rec.time_position - end_time
            if pad_duration < 0:
                raise Exception('for rec %s, time_position < end_time? %f %f'%
                    (rec,rec.time_position,end_time))
            self._pad_file(rec, pad_duration)
            # new_file = rec.edited_version
            new_file = self.edited_audio[rec]
            growing_file = self._concatenate_audio_files(growing_file, new_file)
        end_time = sox.file_info.duration(growing_file.name)
        logger.debug('total edited audio duration  %.2f s'%end_time)
        logger.debug('video duration  %.2f s'%
            self.ref_recording.get_duration())
        return growing_file

    def _pad_or_trim_first_audio(self, first_rec):
        """
        TODO: check if first_rec is a Recording or tempfile (maybe a tempfile if dedrifted)
        NO: will change tempo after trimming/padding

        Store (into Recording.edited_audio dict) the handle  of the sox processed
        first recording, padded or chopped according to AudioStitcherVideoMerger.ref_recording
        starting time. Length of the written file can differ from length of the
        submitted Recording object if drift is corrected with sox tempo
        transform, so check it with sox.file_info.duration()
        """
        logger.debug(' editing %s'%first_rec)
        audio_start  = first_rec.get_start_time()
        ref_start = self.ref_recording.get_start_time()
        if ref_start < audio_start: # padding
            logger.debug('padding')
            pad_duration  = (audio_start-ref_start).total_seconds()
            """padding first_file:
                    ┏━━━━━━━━━━━━━━━┓
                    ┗━━━━━━━━━━━━━━━┛ref
                      ┏━━━━━━┓
                    ┣━┻━━━━━━┛
            """
            self._pad_file(first_rec, pad_duration)
        else:
            logger.debug('trimming')
            length = (ref_start-audio_start).total_seconds()
            """chopping first_file:
                    ┏━━━━━━━━━━━━━━━┓
                    ┗━━━━━━━━━━━━━━━┛ref
                  ┏━╋━━━━┓
                  ┗━┻━━━━┛
            """
            self._chop_file(first_rec, length)
        return

    def _concatenate_audio_files(self, f1, f2):
        # return a tmp file object resulting in f1 f2 concatenation
        # on exit f1 and f2 are closed()
        cbn = sox.Combiner()
        out_file = tempfile.NamedTemporaryFile(suffix='.wav',  delete=DEL_TEMP)
        out_file_name = out_file.name
        status = cbn.build(
            [f1.name, f2.name],
            out_file_name,
            combine_type='concatenate',
            )
        logger.debug('sox.build exit code %s'%str(status))
        f1.close()
        f2.close()
        return out_file

    def _pad_file(self, recording, pad_duration):
        # set recording.edited_version to the handle file a sox padded audio
        logger.debug('sox_transform.pad arg: %f secs'%pad_duration)
        sox_transform = sox.Transformer()
        sox_transform.pad(pad_duration)
        self._edit_audio_file(recording, sox_transform)

    def _chop_file(self, recording, length):
        # set recording.edited_version to the handle file a sox chopped audio
        sox_transform = sox.Transformer()
        sox_transform.trim(length)
        logger.debug('sox_transform.trim arg: %f secs'%length)
        self._edit_audio_file(recording, sox_transform)

    def _edit_audio_file(self, audio_rec, sox_transform):
        """
        Apply the specified sox_transform onto the audio_rec and update
        self.edited_audio dict with the result (with audio_rec as the key)
        """
        output_fh = tempfile.NamedTemporaryFile(suffix='.wav', delete=DEL_TEMP)
        logger.debug('transform: %s'%sox_transform.effects)
        recording_fh = self.edited_audio[audio_rec]
        logger.debug('for recording %s, matching %s'%(audio_rec,
                                                self.ref_recording))
        input_file = _pathname(recording_fh)
        logger.debug('AudioStitcherVideoMerger.edited_audio[audio_rec]: %s'%
                                                    input_file)
        out_file = _pathname(output_fh)
        logger.debug('sox in and out files: %s %s'%(input_file, out_file))
        status = sox_transform.build(input_file, out_file, return_output=True )
        logger.debug('sox.build exit code %s'%str(status))
        # audio_rec.edited_version = output_fh
        self.edited_audio[audio_rec] = output_fh

    # def _write_ISOs_for(self, synced_clip_file, device, dev_joined_audio):
    #     """
    #     Writes isolated audio files that were synced to synced_clip_file,
    #     each track will have its dedicated monofile, named sequentially or with
    #     the name find in TRACKSFN if any, see Scanner._get_tracks_from_file()

    #     synced_clip_file:
    #         video to which audio has been merged
    #     device:
    #         instance of device_scanner.Device
    #     dev_joined_audio:
    #         NamedTemporaryFile for the joined synced (multi channel) audio for
    #         a specific device

    #     Returns nothing, output is written to filesystem as below.
    #     ISOs subfolders structure when user invokes the --isos flag:

    #     SyncedMedia/ (or output_dir)

    #             leftCAM/

    #                 canon24fps01.MOV ━━━━┓ name of clip is name of folder
    #                 canon24fps01.ISO/ <━━┛
    #                     chan_1.wav     
    #                     chan_2.wav     
    #                 canon24fps02.MOV 
    #                 canon24fps01.ISO/ 
    #                     chan_1.wav
    #                     chan_2.wav

    #             rightCAM/
    #     """
    #     def _trim_end(fh, length):
    #         # length in seconds
    #         sox_transform = sox.Transformer()
    #         sox_transform.trim(0, length)
    #         logger.debug('args: %s %s'%(fh, length))
    #         output_fh = tempfile.NamedTemporaryFile(suffix='.wav',
    #                                                 delete=DEL_TEMP)
    #         logger.debug('transform: %s'%sox_transform.effects)
    #         input_file = _pathname(fh)
    #         out_file = _pathname(output_fh)
    #         logger.debug('sox in and out files: %s %s'%(input_file, out_file))
    #         status = sox_transform.build(input_file, out_file,
    #                                             return_output=True )
    #         logger.debug('sox.build exit code %s'%str(status))
    #         shutil.copy(out_file, input_file)
    #     synced_clip_dir = synced_clip_file.parent
    #     # build ISOs subfolders structure, see comment string below
    #     video_stem_WO_suffix = synced_clip_file.stem
    #     # video_stem_WO_suffix = synced_clip_file.stem.split('.')[0]
    #     # OUT_DIR_DEFAULT, D2 = ISOsDIR.split('/')
    #     ISOdir = synced_clip_dir/(video_stem_WO_suffix + '.ISO')
    #     os.makedirs(ISOdir, exist_ok=True)
    #     ISO_multi_chan = ISOdir / 'ISO_multi_chan.wav'
    #     logger.debug('temp file: %s'%(ISO_multi_chan))
    #     logger.debug('will split audio to %s'%(ISOdir))
    #     shutil.copy(_pathname(dev_joined_audio), ISO_multi_chan)
    #     ref_duration = self.ref_recording.get_duration()
    #     logger.debug('ref_duration %s (%s)'%(ref_duration,self.ref_recording))
    #     _trim_end(ISO_multi_chan, ref_duration)
    #     filepath = str(ISO_multi_chan)
    #     nchan = sox.file_info.channels(_pathname(dev_joined_audio))
    #     logger.debug('nchan of dev_joined_audio %i'%nchan)
    #     if device.tracks:
    #         # track_names = _tracks_list(device.tracks)
    #         track_names = [trk for trk in device.tracks.rawtrx
    #         if trk not in ['0','ttc', 'tc']]
    #         # eg: ['lav', 'micl', 'micr']
    #     else:
    #         track_names = False
    #     print(' [gold1]%s[/gold1] recorder, tracks: [gold1]%s[/gold1]'%
    #         (device.name, ' '.join(track_names)))
    #     logger.debug('device %s, track_names %s'%(device, track_names))
    #     for n in range(nchan):
    #         if track_names:
    #             if n >= len(track_names):
    #                 tr_name = 'unkown%i'%n + '.wav'
    #             else:
    #                 tr_name = track_names[n] + '.wav'
    #             iso_destination = ISOdir/tr_name
    #         else:
    #             iso_destination = ISOdir/('chan_%i.wav'%n)
    #         logger.debug('iso_destination %s, %i'%(iso_destination, n))
    #         _extr_channel(ISO_multi_chan, iso_destination, n+1)
    #     # tempfiles = _split_channels(ISO_multi_chan)
    #     # mixNnormed = _sox_mix(tempfiles)
    #     # print('516', _pathname(mixNnormed))
    #     os.remove(ISO_multi_chan)

    def _write_ISOs(self, edited_audio_all_devices):
        """
        Writes isolated audio files that were synced to synced_clip_file,
        each track will have its dedicated monofile, named sequentially or with
        the name find in TRACKSFN if any, see Scanner._get_tracks_from_file()

        synced_clip_file:
            video to which audio has been merged
        device:
            instance of device_scanner.Device
        dev_joined_audio:
            NamedTemporaryFile for the joined synced (multi channel) audio for
            a specific device

        Returns nothing, output is written to filesystem as below.
        ISOs subfolders structure when user invokes the --isos flag:

        SyncedMedia/ (or output_dir)

                leftCAM/

                    canon24fps01.MOV ━━━━┓ name of clip is name of folder
                    canon24fps01.ISO/ <━━┛
                        chan_1.wav     
                        chan_2.wav     
                    canon24fps02.MOV 
                    canon24fps01.ISO/ 
                        chan_1.wav
                        chan_2.wav

                rightCAM/
        """
        def _fit_length(audio_tempfile) -> tempfile.NamedTemporaryFile:
            """            
            Changes the length of audio contained in audio_tempfile so it is the
            same as video length associated with this AudioStitcherVideoMerger.
            Returns a tempfile.NamedTemporaryFile with the new audio
            """         
            sox_transform = sox.Transformer()
            audio_length = sox.file_info.duration(_pathname(audio_tempfile))
            video_length = self.ref_recording.get_duration()
            if audio_length > video_length:
                # trim audio
                sox_transform.trim(0, video_length)
            else:
                # pad audio
                sox_transform.pad(0, video_length - audio_length)
            out_tf = tempfile.NamedTemporaryFile(suffix='.wav',
                                                    delete=DEL_TEMP)
            logger.debug('transform: %s'%sox_transform.effects)
            input_file = _pathname(audio_tempfile)
            out_file = _pathname(out_tf)
            logger.debug('sox in and out files: %s %s'%(input_file, out_file))
            status = sox_transform.build(input_file, out_file,
                                                return_output=True )
            logger.debug('sox.build exit code %s'%str(status))
            logger.debug('audio duration  %.2f s'%
                sox.file_info.duration(_pathname(out_tf)))
            logger.debug('video duration  %.2f s'%
                self.ref_recording.get_duration())
            return out_tf
        synced_clip_file = self.ref_recording.final_synced_file
        synced_clip_dir = synced_clip_file.parent
        # build ISOs subfolders structure, see comment string below
        video_stem_WO_suffix = synced_clip_file.stem
        # video_stem_WO_suffix = synced_clip_file.stem.split('.')[0]
        # OUT_DIR_DEFAULT, D2 = ISOsDIR.split('/')
        ISOdir = synced_clip_dir/(video_stem_WO_suffix + '.ISO')
        os.makedirs(ISOdir, exist_ok=True)
        logger.debug('edited_audio_all_devices %s'%edited_audio_all_devices)
        logger.debug('ISOdir %s'%ISOdir)
        # ISO_multi_chan = ISOdir / 'ISO_multi_chan.wav'
        # logger.debug('temp file: %s'%(ISO_multi_chan))
        # logger.debug('will split audio to %s'%(ISOdir))
        for name, audio_tempfile in edited_audio_all_devices:
             # pad(start_duration: float = 0.0, end_duration: float = 0.0)[source]
            destination = ISOdir/('%s.wav'%name)
            audio_tempfile_trimpad = _fit_length(audio_tempfile)
            shutil.copy(_pathname(audio_tempfile_trimpad), destination)
            logger.debug('destination:%s'%destination)
        # ref_duration = self.ref_recording.get_duration()
        # logger.debug('ref_duration %s (%s)'%(ref_duration,self.ref_recording))
        # _trim_end(ISO_multi_chan, ref_duration)
        # filepath = str(ISO_multi_chan)
        # nchan = sox.file_info.channels(_pathname(dev_joined_audio))
        # logger.debug('nchan of dev_joined_audio %i'%nchan)
        # if device.tracks:
        #     # track_names = _tracks_list(device.tracks)
        #     track_names = [trk for trk in device.tracks.rawtrx
        #     if trk not in ['0','ttc', 'tc']]
        #     # eg: ['lav', 'micl', 'micr']
        # else:
        #     track_names = False
        # print(' [gold1]%s[/gold1] recorder, tracks: [gold1]%s[/gold1]'%
        #     (device.name, ' '.join(track_names)))
        # logger.debug('device %s, track_names %s'%(device, track_names))
        # for n in range(nchan):
        #     if track_names:
        #         if n >= len(track_names):
        #             tr_name = 'unkown%i'%n + '.wav'
        #         else:
        #             tr_name = track_names[n] + '.wav'
        #         iso_destination = ISOdir/tr_name
        #     else:
        #         iso_destination = ISOdir/('chan_%i.wav'%n)
        #     logger.debug('iso_destination %s, %i'%(iso_destination, n))
        #     _extr_channel(ISO_multi_chan, iso_destination, n+1)
        # # tempfiles = _split_channels(ISO_multi_chan)
        # # mixNnormed = _sox_mix(tempfiles)
        # # print('516', _pathname(mixNnormed))
        # os.remove(ISO_multi_chan)

    def build_audio_and_write_video(self, top_dir, output_dir,
                                    write_multicam_structure,
                                    asked_ISOs):
        """
        top_dir: Path, directory where media were looked for

        output_dir: str for optional folder specified as CLI argument, if
        value is None, fall back to OUT_DIR_DEFAULT

        write_multicam_structure: True if needs to write multicam folders

        asked_ISOs: bool flag specified as CLI argument

        For each audio devices found overlapping self.ref_recording: pad, trim
        or stretch audio files calling _get_concatenated_audiofile_for(), and
        put them in merged_audio_files_by_device. More than one audio recorder
        can be used for a shot: that's why merged_audio_files_by_device is a
        list

        Returns nothing

        Sets AudioStitcherVideoMerger.final_synced_file on completion
        """
        logger.debug(' fct args: top_dir: %s; output_dir: %s; write_multicam_structure: %s; asked_ISOs: %s;'%
            (top_dir, output_dir, write_multicam_structure, asked_ISOs))
        logger.debug('device for rec %s: %s'%(self.ref_recording,
            self.ref_recording.device))
        # suppose the user called tictacsync with 'mondayPM' as top folder to
        # scan for dailies (and 'somefolder' for output):
        if output_dir == None:
            synced_clip_dir = Path(top_dir)/OUT_DIR_DEFAULT # = mondayPM/SyncedMedia
        else:
            synced_clip_dir = Path(output_dir)/Path(top_dir).name # = somefolder/mondayPM
        if write_multicam_structure:
            device_name = self.ref_recording.device.name
            synced_clip_dir = synced_clip_dir/device_name # = synced_clip_dir/ZOOM
        self.synced_clip_dir = synced_clip_dir
        os.makedirs(synced_clip_dir, exist_ok=True)
        logger.debug('synced_clip_dir is: %s'%synced_clip_dir)
        synced_clip_file = synced_clip_dir/\
            Path(self.ref_recording.new_rec_name).name
        logger.debug('editing files for %s'%synced_clip_file)
        # collecting edited audio by device, in (Device, tempfile) pairs:
        merged_audio_files_by_device = [
                            (d, self._get_concatenated_audiofile_for(d)) 
                            for d in self._get_audio_devices()]
        if len(merged_audio_files_by_device) == 0:
            # no audio file overlaps for this clip
            return
        # split audio channels in mono wav tempfiles:    
        edited_audio_all_devices = []
        for device, multi_chan_audio in merged_audio_files_by_device:
            mono_files = _split_channels(multi_chan_audio)
            logger.debug('%i mono files for %s'%(len(mono_files), device.name))
            dev_audio_tuples = [(device, idx, m) for idx, m
                                            in enumerate(mono_files)]
            edited_audio_all_devices += dev_audio_tuples
        multiple_recorders = len(merged_audio_files_by_device) > 1
        logger.debug('multiple_recorder: %s'%multiple_recorders)
        # replace device, idx pair with track name (+ device name if many)
        def _trnm(dev, idx): # used in the list comprehension just below
            if dev.tracks == None:
                tag = 'chan%s'%str(idx+1).zfill(2)
            else:
                audio_tags = [tag for tag in dev.tracks.rawtrx
                    if tag not in ['ttc','0','tc']]
                tag = audio_tags[idx]
            if multiple_recorders:
                tag += '_' + dev.name
            return tag
        edited_audio_all_devices = [(_trnm(dev, idx), audio_tempfile)
                    for dev, idx, audio_tempfile in edited_audio_all_devices]
        logger.debug('edited_audio_all_devices %s'%edited_audio_all_devices)
        video_path = self.ref_recording.AVpath
        # stacked audio contains all audio recorders if many
        mixed_audio = _sox_combine([audio for _, audio
                in merged_audio_files_by_device]) # all devices
        logger.debug('will merge with %s'%(_pathname(mixed_audio)))
        self.ref_recording.synced_audio = mixed_audio
        nchan = sox.file_info.channels(_pathname(mixed_audio))
        logger.debug('mixed_audio n chan: %i'%nchan)
        self.ref_recording.final_synced_file = synced_clip_file # relative
        self._merge_audio_and_video()
        if asked_ISOs:
            self._write_ISOs(edited_audio_all_devices)
        logger.debug('merged_audio_files_by_device %s'%
            merged_audio_files_by_device)
        for idx, pair in enumerate(merged_audio_files_by_device): # This loop for logging purpose only.
            # dev_joined_audio is mono, stereo or even polywav from multitrack 
            # recorders. For one video there could be more than one dev_joined_audio
            # if multiple audio recorders where used during the take.
            # this loop is for one device at the time.
            device, dev_joined_audio = pair
            logger.debug('idx: % i device.folder: %s'%(idx, device.folder))
            nchan = sox.file_info.channels(_pathname(dev_joined_audio))
            logger.debug('dev_joined_audio: %s nchan:%i'%
                (_pathname(dev_joined_audio), nchan))
            logger.debug('duration %f s'%
                sox.file_info.duration(_pathname(dev_joined_audio)))
        # generates ISOs too
        # if asked_ISOs:
        #     print('Writing ISO files for:')
        #     for idx, pair in enumerate(merged_audio_files_by_device):
        #         device, dev_joined_audio = pair
        #         logger.debug('device %i, dev_joined_audio %s %s'%
        #             (idx, device, _pathname(dev_joined_audio)))
        #         self._write_ISOs_for(synced_clip_file,
        #             device, dev_joined_audio)

    def _keep_VIDEO_only(self, video_path):
        # return file handle to a temp video file formed from the video_path
        # stripped of its sound
        in1 = ffmpeg.input(_pathname(video_path))
        video_extension = video_path.suffix
        silenced_opts = ["-loglevel", "quiet", "-nostats", "-hide_banner"]
        file_handle = tempfile.NamedTemporaryFile(suffix=video_extension,
            delete=DEL_TEMP)
        out1 = in1.output(file_handle.name, map='0:v', vcodec='copy')
        ffmpeg.run([out1.global_args(*silenced_opts)], overwrite_output=True)
        return file_handle
        # os.path.split audio channels if more than one

    def _merge_audio_and_video(self):
        """      
        Calls ffmpeg to join audio and video.

        On entry, ref_recording.final_synced_file is a Path to an non existing
        file (contrarily to ref_recording.synced_audio).
        On exit, ref_recording.final_synced_file points to the final synced
        video file. Returns nothing.
        """
        synced_clip_file = self.ref_recording.final_synced_file
        video_path = self.ref_recording.AVpath
        timecode = self.ref_recording.get_timecode()
        # self.ref_recording.synced_audio = audio_path
        audio_path = self.ref_recording.synced_audio
        vid_only_handle = self._keep_VIDEO_only(video_path)
        a_n = _pathname(audio_path)
        v_n = str(vid_only_handle.name)
        out_n = str(synced_clip_file)
        logger.debug('Merging: \n\t %s + %s = %s\n'%(
                        audio_path,
                        video_path,
                        synced_clip_file
                        ))
        # building args for debug purpose only:
        ffmpeg_args = (
            ffmpeg
            .input(v_n)
            .output(out_n, shortest=None, vcodec='copy',
                timecode=timecode)
            .global_args('-i', a_n, "-hide_banner")
            .overwrite_output()
            .get_args()
        )
        logger.debug('ffmpeg args: %s'%' '.join(ffmpeg_args))
        try: # for real now
            _, out = (
            ffmpeg
            .input(v_n)
            .output(out_n, shortest=None, vcodec='copy',
                # metadata='reel_name=foo', not all container support gen MD
                timecode=timecode,
                )
            .global_args('-i', a_n, "-hide_banner")
            .overwrite_output()
            .run(capture_stderr=True)
            )
            logger.debug('ffmpeg output')
            for l in out.decode("utf-8").split('\n'):
                logger.debug(l)
        except ffmpeg.Error as e:
            print('ffmpeg.run error merging: \n\t %s + %s = %s\n'%(
                audio_path,
                video_path,
                synced_clip_file
                ))
            print(e)
            print(e.stderr.decode('UTF-8'))
            sys.exit(1)


class Matcher:
    """
    Matcher looks for any video in self.recordings and for each one finds out
    all audio recordings (again in self.recordings) that time overlap
    (or against any designated 'main sound', see below). It then spawns
    AudioStitcherVideoMerger objects that do the actual file manipulations. Each video
    (and main sound) will have its AudioStitcherVideoMerger instance.

    All videos are de facto reference recording and matching audio files are
    looked up for each one of them.

    The Matcher doesn't keep neither set any editing information in itself: the
    in and out time values (UTC times) used are those kept inside each Recording
    instances.

    [NOT YET IMPLEMENTED]: When shooting is done with multiple audio recorders,
    ONE audio device can be designated as 'main sound' and used as reference
    recording; then all audio tracks are synced together against this main
    sound audio file, keeping the TicTacCode track alongside for syncing against
    their video counterpart(in a second pass and after a mixdown editing).
    [/NOT YET IMPLEMENTED]

    Attributes:

        recordings : list of Recording instances
            all the scanned recordings with valid TicTacCode, set in __init__()

        video_mergers : list
            of AudioStitcherVideoMerger Class instances, built by
            scan_audio_for_each_ref_rec(); each video has a corresponding
            AudioStitcherVideoMerger object. An audio_stitch doesn't extend
            beyond the corresponding video start and end times.

    """

    def __init__(self, recordings_list):
        """        
        At this point in the program, all recordings in recordings_list should
        have a valid Recording.start_time attribute and one of its channels
        containing a TicTacCode signal (which the start_time has been demodulated
        from)
        
        """
        self.recordings = recordings_list
        self.video_mergers = []

    def _rename_all_recs(self):
        """
        Add _synced to filenames of synced video files. Change stored name only:
        files have yet to be written to.
        """
        # match IO_structure:
            # case 'foldercam':
        for rec in self.recordings:
            rec_extension = rec.AVpath.suffix
            rel_path_new_name = '%s%s'%(rec.AVpath.stem, rec_extension)
            rec.new_rec_name = Path(rel_path_new_name)
            logger.debug('for %s new name: %s'%(
                _pathname(rec.AVpath),
                _pathname(rec.new_rec_name)))

    def scan_audio_for_each_ref_rec(self):
        """
        For each video (and for the Main Sound) in self.recordings, this finds
        any audio that has overlapping times and instantiates a
        AudioStitcherVideoMerger object.

        V1 checked against A1, A2, A3, A4
        V2 checked against A1, A2, A3, A4
        V3 checked against    ...
        Main Sound checked against A1, A2, A3, A4
        """
        refeference_recordings = [r for r in self.recordings if r.is_video()
                                                            or r.is_reference]
        audio_recs = [r for r in self.recordings if r.is_audio()
                                                and not r.is_reference]
        if not audio_recs:
            print('\nNo audio recording found, syncing of videos only not implemented yet, exiting...\n')
            sys.exit(1)
        for ref_rec in refeference_recordings:
            reference_tag = 'video' if ref_rec.is_video() else 'audio'
            logger.debug('Looking for overlaps with %s %s'%(
                            reference_tag,
                            ref_rec))
            audio_stitch = AudioStitcherVideoMerger(ref_rec)
            for audio in audio_recs:
                if self._does_overlap(ref_rec, audio):
                    audio_stitch.add_matched_audio(audio)
                    logger.debug('recording %s overlaps,'%(audio))
                    # print('  recording [gold1]%s[/gold1] overlaps,'%(audio))
            if len(audio_stitch.get_matched_audio_recs()) > 0:
                self.video_mergers.append(audio_stitch)
            else:
                logger.debug('\n  nothing\n')
                print('No overlap found for %s'%ref_rec.AVpath.name)
                del audio_stitch
        logger.debug('%i video_mergers created'%len(self.video_mergers))

    def _does_overlap(self, ref_rec, audio_rec):
        A1, A2 = audio_rec.get_start_time(), audio_rec.get_end_time()
        R1, R2 = ref_rec.get_start_time(), ref_rec.get_end_time()
        no_overlap = (A2 < R1) or (A1 > R2)
        return not no_overlap

    def shrink_gaps_between_takes(self, with_gap=CLUSTER_GAP):
        """
        for single cam shootings this simply sets the gap between takes,
        tweaking each vid timecode metadata to distribute them next to each
        other along NLE timeline. For multicam takes, shifts are computed so
        video clusters are near but dont overlap, ex: 

        Cluster 1           Cluster 2
        1111111111111        2222222222 (cam A)
           11111111111[...]222222222 (cam B)

        or
        1111111111111    222222 (cam A)
          1111111     22222 (cam B)

        Returns nothing, changes are done in the video files metadata
        (each referenced by Recording.final_synced_file)
        """
        vids = [m.ref_recording for m in self.video_mergers]
        logger.debug('vids %s'%vids)
        if len(vids) == 1:
            logger.debug('just one take, no gap to shrink')
            return
        # INs_and_OUTs contains (time, direction, video) for each video,
        # where direction is 'in|out' and video an instance of Recording
        INs_and_OUTs = [(vid.get_start_time(), 'in', vid) for vid in vids]
        for vid in vids:
            INs_and_OUTs.append((vid.get_end_time(), 'out', vid))
        INs_and_OUTs = sorted(INs_and_OUTs, key=lambda vtuple: vtuple[0])
        logger.debug('INs_and_OUTs: %s'%INs_and_OUTs)
        new_cluster = True
        current_cluster = {'vids':[]}
        N_in, N_out = (0, 0)
        # clusters is a list of  {'end': t1, 'start': t2, 'vids': [r1,r3]}
        clusters = []
        for t, direction, video in INs_and_OUTs:
            if new_cluster and direction == 'out':
                logger.error('cant begin a cluster with a out time %s'%video)
                sys.exit(1)
            if new_cluster:
                current_cluster['start'] = t
                new_cluster = False
            if direction == 'in':
                N_in += 1
                current_cluster['vids'].append(video)
            else:
                N_out += 1
            N_currently_open = N_in - N_out
            if N_currently_open == 0:
                # print(t,direction,video)
                current_cluster['end'] = t
                clusters.append(current_cluster)
                new_cluster = True
                current_cluster = {'vids':[]}
                N_in, N_out = (0, 0)
        logger.debug('clusters: %s'%pprint.pformat(clusters))
        # if there are N clusters, there are N-1 gaps to evaluate and shorten
        # (lengthen?) to a value of with_gap seconds
        gaps = [c2['start'] - c1['end'] for c1, c2
                                    in zip(clusters, clusters[1:])]
        logger.debug('gaps between clusters %s'%[g.total_seconds()
            for g in gaps])
        logger.debug('desired gap is %f'%with_gap)
        # if gap is 3.5s and goal is 2s (the with_gap parameter), clip has to
        # move 1.5s *to the left* ie towards negative axis of time, so the
        # offset should be negative too
        offsets = [timedelta(seconds=with_gap) - gap for gap in gaps]
        logger.debug('gap difference: %s'%[o.total_seconds() for o in offsets])
        zero = [timedelta(seconds=0)] # for the first cluster
        cummulative_offsets = zero + list(numpy.cumsum(offsets))
        # for now on, offsets are in secs, not timedeltas
        cummulative_offsets = [td.total_seconds() for td in cummulative_offsets]
        logger.debug('cummulative_offsets: %s'%cummulative_offsets)
        time_of_first = clusters[0]['start']
        offset_for_all_clips = - from_midnight(time_of_first).total_seconds()
        logger.debug('time_of_first: %s'%time_of_first)
        logger.debug('offset_for_all_clips: %s'%offset_for_all_clips)
        for cluster, offset in zip(clusters, cummulative_offsets):
            total_offset = offset + offset_for_all_clips
            logger.debug('for %s offset in sec: %f'%(cluster['vids'],
                    total_offset))
            for vid in cluster['vids']:
                tc = vid.get_timecode(with_offset=total_offset)
                logger.debug('for %s old tc: %s new tc %s'%(vid,
                    vid.get_timecode(), tc))
                vid.write_file_timecode(tc)
        return


















