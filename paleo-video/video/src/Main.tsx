import {AbsoluteFill, Audio, Img, Sequence, interpolate, random, staticFile, useCurrentFrame, Easing} from 'remotion';
import {Subtitles} from './Subtitles';

export const FPS = 30;
const AUDIO_END = 114.3;
export const TOTAL_FRAMES = Math.round((AUDIO_END + 1.2) * FPS);
const FADE = 24;

// Scene start times (seconds) aligned to the narration
const SCENES: {img: string; at: number}[] = [
	{img: 's01', at: 0},
	{img: 's15', at: 9.9},
	{img: 's02', at: 16.2},
	{img: 's03', at: 20.4},
	{img: 's04', at: 24.5},
	{img: 's05', at: 34.3},
	{img: 's06', at: 43.2},
	{img: 's07', at: 49.8},
	{img: 's08', at: 60.6},
	{img: 's09', at: 64.2},
	{img: 's10', at: 72.2},
	{img: 's11', at: 83.8},
	{img: 's12', at: 93.0},
	{img: 's13', at: 106.1},
];

const KenBurns: React.FC<{img: string; dur: number; index: number}> = ({img, dur, index}) => {
	const frame = useCurrentFrame();
	const t = interpolate(frame, [0, dur], [0, 1], {extrapolateRight: 'clamp', easing: Easing.inOut(Easing.quad)});
	const zoomIn = index % 2 === 0;
	const scale = zoomIn ? 1.06 + 0.12 * t : 1.18 - 0.12 * t;
	const dir = index % 4 < 2 ? 1 : -1;
	const x = dir * (t - 0.5) * 50;
	const y = (index % 3 === 0 ? -1 : 1) * (t - 0.5) * 20;
	const opacity = interpolate(frame, [0, FADE], [0, 1], {extrapolateRight: 'clamp'});
	return (
		<AbsoluteFill style={{opacity}}>
			<Img
				src={staticFile(`images/${img}.png`)}
				style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${scale}) translate(${x}px, ${y}px)`}}
			/>
		</AbsoluteFill>
	);
};

const Dust: React.FC = () => {
	const frame = useCurrentFrame();
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			{new Array(40).fill(0).map((_, i) => {
				const speed = 0.15 + random(`s${i}`) * 0.35;
				const x = (random(`x${i}`) * 1920 + frame * speed * (random(`d${i}`) > 0.5 ? 1 : -1)) % 1920;
				const y = (random(`y${i}`) * 1080 - frame * speed * 0.6 + 1080 * 4) % 1080;
				const size = 1.5 + random(`z${i}`) * 3;
				const flicker = 0.25 + 0.35 * Math.sin(frame / 20 + i);
				return (
					<div
						key={i}
						style={{position: 'absolute', left: (x + 1920) % 1920, top: y, width: size, height: size, borderRadius: '50%', background: 'rgba(255,236,200,1)', opacity: flicker, filter: 'blur(0.6px)'}}
					/>
				);
			})}
		</AbsoluteFill>
	);
};

const Grade: React.FC = () => {
	const frame = useCurrentFrame();
	return (
		<>
			<AbsoluteFill style={{background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(10,6,2,0.65) 100%)'}} />
			<AbsoluteFill style={{background: 'linear-gradient(to bottom, rgba(0,0,0,0) 70%, rgba(0,0,0,0.55) 100%)'}} />
			<AbsoluteFill style={{opacity: 0.07, mixBlendMode: 'overlay'}}>
				<svg width="1920" height="1080">
					<filter id="grain">
						<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed={frame % 12} />
					</filter>
					<rect width="100%" height="100%" filter="url(#grain)" />
				</svg>
			</AbsoluteFill>
		</>
	);
};

export const Main: React.FC = () => {
	const frame = useCurrentFrame();
	const fadeOut = interpolate(frame, [TOTAL_FRAMES - 36, TOTAL_FRAMES], [1, 0], {extrapolateLeft: 'clamp'});
	const fadeIn = interpolate(frame, [0, 20], [0, 1], {extrapolateRight: 'clamp'});
	return (
		<AbsoluteFill style={{backgroundColor: '#000'}}>
			<AbsoluteFill style={{opacity: Math.min(fadeIn, fadeOut)}}>
				{SCENES.map((s, i) => {
					const from = Math.round(s.at * FPS);
					const end = i < SCENES.length - 1 ? Math.round(SCENES[i + 1].at * FPS) + FADE : TOTAL_FRAMES;
					return (
						<Sequence key={s.img} from={from} durationInFrames={end - from}>
							<KenBurns img={s.img} dur={end - from} index={i} />
						</Sequence>
					);
				})}
				<Dust />
				<Grade />
			</AbsoluteFill>
			<Subtitles />
			<Audio src={staticFile('voice.mp3')} />
		</AbsoluteFill>
	);
};
