import {installWhisperCpp, downloadWhisperModel, transcribe, toCaptions} from '@remotion/install-whisper-cpp';
import fs from 'node:fs';
const dir = process.argv[2], wav = process.argv[3], out = process.argv[4];
await installWhisperCpp({to: dir, version: '1.7.6'});
await downloadWhisperModel({model: 'large-v3-turbo', folder: dir});
const r = await transcribe({inputPath: wav, whisperPath: dir, whisperCppVersion: '1.7.6', model: 'large-v3-turbo', tokenLevelTimestamps: true, language: 'ja', splitOnWord: true});
const {captions} = toCaptions({whisperCppOutput: r});
fs.writeFileSync(out, JSON.stringify(captions, null, 1));
console.log('captions', captions.length);
