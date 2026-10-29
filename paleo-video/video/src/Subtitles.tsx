import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont} from '@remotion/google-fonts/NotoSerifJP';
import captions from './captions.json';

const {fontFamily} = loadFont('normal', {weights: ['600'], ignoreTooManyRequestsWarning: true});

export const Subtitles: React.FC<{boxed?: boolean}> = ({boxed}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;
	const active = [...captions].reverse().find((c) => t >= c.start && t < c.end);
	if (!active) return null;
	const local = (t - active.start) * fps;
	const opacity = interpolate(local, [0, 6], [0, 1], {extrapolateRight: 'clamp'});
	return (
		<AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 70}}>
			<div
				style={{
					fontFamily,
					fontWeight: 600,
					fontSize: 46,
					lineHeight: 1.45,
					color: '#fbf3e4',
					maxWidth: 1500,
					textAlign: 'center',
					opacity,
					textShadow: '0 2px 4px rgba(0,0,0,0.9), 0 0 18px rgba(0,0,0,0.7)',
					letterSpacing: 1,
					textWrap: 'balance',
					...(boxed ? {background: 'rgba(22,15,8,0.78)', padding: '10px 28px', borderRadius: 6, fontSize: 42} : {}),
				}}
			>
				{active.text}
			</div>
		</AbsoluteFill>
	);
};
