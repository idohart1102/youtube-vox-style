import {Composition} from 'remotion';
import {Main, FPS, TOTAL_FRAMES} from './Main';
import {Vox, VOX_FPS, VOX_FRAMES} from './vox/Vox';

export const RemotionRoot: React.FC = () => (
	<>
		<Composition id="Main" component={Main} durationInFrames={TOTAL_FRAMES} fps={FPS} width={1920} height={1080} />
		<Composition id="Vox" component={Vox} durationInFrames={VOX_FRAMES} fps={VOX_FPS} width={1920} height={1080} />
	</>
);
