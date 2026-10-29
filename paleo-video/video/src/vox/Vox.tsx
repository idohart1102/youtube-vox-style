import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Subtitles} from '../Subtitles';
import {Card, Clock, Counter, Cutout, Draw, Label, Paper, Pin, Stamp, circlePath, useSec} from './kit';

export const VOX_FPS = 30;
const END = 115.5;
export const VOX_FRAMES = Math.round(END * VOX_FPS);
const OVERLAP = 0.5;

// Scenes take absolute narration times; everything inside uses absolute seconds too (via `T`)
const S1: React.FC<{T: number}> = ({T}) => (
	<>
		<Paper />
		<Cutout src="earth" x={760} y={560} w={640} at={0.1 - T} />
		<Draw d="M1900,40 C1600,120 1250,250 1010,430" at={0.4 - T} dur={1.6} dashed width={9} />
		<Cutout src="asteroid" x={1950} y={-60} w={300} at={0.3 - T} move={{to: [1180, 330], from: 0.4 - T, dur: 1.8}} />
		<Draw d="M1180,330 C1050,250 900,200 640,190" at={2.2 - T} dur={0.8} dashed width={7} arrow />
		<Label text="30分早い" x={560} y={140} at={2.4 - T} tone="white" rot={-3} until={6.9 - T} />
		<Draw d="M1180,330 C1250,520 1300,700 1420,860" at={4.5 - T} dur={0.8} dashed width={7} arrow />
		<Label text="30分遅い" x={1640} y={720} at={4.6 - T} tone="white" rot={2} until={6.9 - T} />
		<Label text="地球の歴史は全く違うものに" x={960} y={80} at={7.0 - T} size={62} />
	</>
);

const S2: React.FC<{T: number}> = ({T}) => (
	<>
		<Paper />
		<Cutout src="human" x={520} y={540} w={760} at={10.1 - T} />
		<Draw d="M330,260 L720,800" at={10.6 - T} dur={0.35} width={22} />
		<Draw d="M720,260 L330,800" at={10.9 - T} dur={0.35} width={22} />
		<Label text="人類は誕生せず？" x={520} y={150} at={10.5 - T} tone="white" />
		<Cutout src="sauropod" x={1380} y={500} w={820} at={12.1 - T} enter="right" />
		<Cutout src="raptor" x={1130} y={700} w={380} at={12.6 - T} />
		<Label text="支配者は恐竜のまま" x={1380} y={160} at={13.5 - T} size={60} />
	</>
);

const S3: React.FC<{T: number}> = ({T}) => {
	const t = useSec() + T;
	return (
		<>
			<Paper />
			{t < 20.2 ? (
				<>
					<Counter to={66000000} suffix="年前" x={960} y={170} at={16.2 - T} />
					<Label text="春" x={1490} y={250} at={17.7 - T} tone="red" rot={4} />
					<Cutout src="map_na" x={960} y={620} w={760} at={17.9 - T} />
					<Pin x={MAP_NA_PIN[0]} y={MAP_NA_PIN[1]} at={18.6 - T} />
					<Label text="北アメリカ" x={MAP_NA_PIN[0] + 260} y={MAP_NA_PIN[1] - 40} at={18.8 - T} tone="white" />
				</>
			) : null}
			<Card src="bg_forest" x={960} y={540} w={1780} at={19.7 - T} rot={-0.8} />
			<Cutout src="trex" x={2300} y={600} w={1050} at={20.4 - T} enter="right" flip move={{to: [1050, 600], from: 20.6 - T, dur: 3.2, ease: false}} bob={14} />
			<Label text="地上最強の捕食者" x={560} y={160} at={20.8 - T} size={62} />
			<Label text="ティラノサウルス" x={620} y={260} at={22.0 - T} tone="white" rot={1} />
		</>
	);
};

const S4: React.FC<{T: number}> = ({T}) => (
	<>
		<Paper />
		<Card src="bg_ground" x={960} y={560} w={1700} at={24.4 - T} enter="bottom" rot={0.6} push={0.03} objPos="50% 60%" />
		<Cutout src="trex_foot" x={700} y={230} w={520} at={24.8 - T} enter="top" />
		<Draw d="M1180,120 L1180,690" at={25.6 - T} dur={1.4} color="#fffaf0" width={9} dashed arrow />
		<Label text="わずか数十cm" x={1440} y={400} at={27.1 - T} />
		<Cutout src="mammal" x={MAMMAL_POS[0]} y={MAMMAL_POS[1]} w={300} at={29.1 - T} tremble={32.6 - T} />
		<Draw d={circlePath(MAMMAL_POS[0], MAMMAL_POS[1], 210, 140)} at={30.6 - T} dur={0.8} />
		<Label text="ネズミほどの哺乳類" x={MAMMAL_POS[0] + 40} y={MAMMAL_POS[1] - 210} at={30.3 - T} tone="white" />
	</>
);

const S5: React.FC<{T: number}> = ({T}) => (
	<>
		<Paper />
		<Card src="bg_wetland" x={960} y={540} w={1780} at={34.2 - T} rot={-0.6} />
		<Label text="水辺の泥の中" x={420} y={130} at={35.3 - T} />
		<Cutout src="turtle" x={560} y={760} w={420} at={37.1 - T} />
		<Label text="小さな亀" x={560} y={560} at={37.4 - T} tone="white" />
		<Cutout src="bird" x={1240} y={660} w={420} at={38.9 - T} rot={-2} />
		<Cutout src="bird" x={1560} y={720} w={330} at={39.6 - T} flip rot={3} />
		<Label text="くちばしを持つ初期の鳥" x={1380} y={380} at={39.4 - T} tone="white" />
	</>
);

const S6: React.FC<{T: number}> = ({T}) => (
	<>
		<Paper />
		<Cutout src="trex" x={1000} y={560} w={1350} at={43.3 - T} enter="bottom" />
		<Cutout src="mammal" x={260} y={900} w={220} at={44.0 - T} />
		<Cutout src="turtle" x={1620} y={930} w={240} at={44.3 - T} />
		<Cutout src="bird" x={1790} y={820} w={220} at={44.6 - T} flip />
		<Label text="この森の誰もが信じていた" x={600} y={110} at={44.0 - T} tone="white" size={46} />
		<Label text="絶対の支配者" x={1300} y={190} at={46.7 - T} size={92} rot={-3} />
	</>
);

const S7: React.FC<{T: number}> = ({T}) => {
	const t = useSec() + T;
	const heat = interpolate(t, [54.4, 56], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const shake = t > 52.3 ? Math.sin(t * 47) * 5 + Math.cos(t * 31) * 4 : 0;
	return (
		<>
			<Paper />
			<div style={{position: 'absolute', inset: 0, transform: `translate(${shake}px, ${shake * 0.6}px)`}}>
				<Card src="bg_inferno" x={960} y={540} w={1800} at={49.8 - T} enter="pop" rot={0.5} push={0.12} />
				<AbsoluteFill style={{background: 'radial-gradient(ellipse at 60% 20%, rgba(255,120,30,0.55), rgba(120,20,0,0.35) 70%)', opacity: heat * (0.75 + 0.25 * Math.sin(t * 9)), mixBlendMode: 'screen'}} />
			</div>
			<Label text="数時間後" x={300} y={120} at={51.3 - T} tone="red" />
			<Draw d="M1500,820 C1200,760 900,800 620,740" at={53.3 - T} dur={0.6} width={16} color="#fffaf0" arrow />
			<Draw d="M1600,940 C1300,900 1000,930 700,880" at={53.5 - T} dur={0.6} width={16} color="#fffaf0" arrow />
			<Label text="川が逆流" x={1500} y={680} at={53.4 - T} />
			<Label text="空が巨大なオーブンに" x={1260} y={150} at={55.6 - T} size={64} />
		</>
	);
};

const S8: React.FC<{T: number}> = ({T}) => (
	<>
		<Paper />
		<Card src="bg_night" x={960} y={540} w={1780} at={60.6 - T} enter="pop" push={0.05} />
		<Cutout src="mammal" x={960} y={820} w={300} at={61.6 - T} enter="bottom" />
		<Label text="その日の夜を迎えられたのは…？" x={960} y={140} at={61.2 - T} tone="white" size={56} />
	</>
);

const TIMELINE_Y = 640;
const S9: React.FC<{T: number}> = ({T}) => (
	<>
		<Paper />
		<Draw d={`M180,${TIMELINE_Y} L1740,${TIMELINE_Y}`} at={64.3 - T} dur={1.6} color="#1d1a16" width={12} />
		<Counter to={165000000} suffix="年" x={900} y={170} at={64.3 - T} dur={1.8} />
		<Label text="恐竜たちの帝国" x={900} y={300} at={67.0 - T} tone="white" />
		<Cutout src="stego" x={380} y={TIMELINE_Y - 150} w={400} at={64.8 - T} dimAt={70.3 - T} />
		<Cutout src="sauropod" x={760} y={TIMELINE_Y - 190} w={460} at={65.3 - T} dimAt={70.4 - T} />
		<Cutout src="triceratops" x={1140} y={TIMELINE_Y - 140} w={400} at={65.8 - T} dimAt={70.5 - T} />
		<Cutout src="trex" x={1520} y={TIMELINE_Y - 150} w={440} at={66.3 - T} dimAt={70.6 - T} />
		<Draw d={`M1760,${TIMELINE_Y - 90} L1790,${TIMELINE_Y + 90}`} at={69.6 - T} dur={0.25} width={22} />
		<Stamp text="たった1日で崩壊" x={1260} y={820} at={69.8 - T} size={96} />
	</>
);

const S10: React.FC<{T: number}> = ({T}) => (
	<>
		<Paper />
		<Label text="最新の研究" x={330} y={140} at={72.7 - T} />
		<Cutout src="fossil" x={760} y={560} w={1000} at={74.9 - T} />
		<Draw d={circlePath(760, 560, 520, 290)} at={76.6 - T} dur={0.9} />
		<Label text="生々しい化石の証拠" x={620} y={240} at={76.8 - T} tone="white" />
		<Clock x={1560} y={470} r={200} at={78.5 - T} spinFrom={80.2 - T} spinDur={3} />
		<Label text="1分・1時間ごとに追体験" x={1520} y={780} at={80.3 - T} size={50} />
	</>
);

const S11: React.FC<{T: number}> = ({T}) => (
	<>
		<Paper />
		<Cutout src="map_gulf" x={900} y={540} w={1500} at={83.9 - T} />
		<Pin x={YUCATAN[0]} y={YUCATAN[1]} at={86.3 - T} />
		<Draw d={circlePath(YUCATAN[0], YUCATAN[1] - 20, 170, 120)} at={86.6 - T} dur={0.8} />
		<Label text="メキシコ・ユカタン半島" x={YUCATAN[0]} y={YUCATAN[1] - 230} at={86.5 - T} />
		<Card src="bg_sea" x={1480} y={760} w={760} at={88.6 - T} rot={4} />
		<Label text="当時は暖かく浅い海" x={1480} y={480} at={90.8 - T} tone="white" />
	</>
);

const S12: React.FC<{T: number}> = ({T}) => (
	<>
		<Paper />
		<Cutout src="strata" x={860} y={580} w={1250} at={93.2 - T} />
		<Label text="ある特別な岩石" x={860} y={120} at={95.6 - T} tone="white" />
		<Draw d="M150,330 L150,900" at={97.4 - T} dur={1.2} color="#1d1a16" width={10} arrow />
		<Draw d="M150,900 L150,330" at={97.4 - T} dur={1.2} color="#1d1a16" width={10} arrow />
		<Label text="厚さ数km" x={210} y={240} at={97.6 - T} rot={-4} />
		<Cutout src="gypsum" x={1640} y={520} w={420} at={102.3 - T} />
		<Draw d="M1460,600 C1300,640 1200,660 1080,640" at={104.2 - T} dur={0.6} width={9} arrow />
		<Label text="石膏の層" x={1640} y={250} at={104.1 - T} size={64} />
		<Label text="カルシウムたっぷり" x={1640} y={790} at={102.9 - T} tone="white" size={44} />
	</>
);

const S13: React.FC<{T: number}> = ({T}) => {
	const t = useSec() + T;
	const shake = t > 112.4 ? Math.sin(t * 60) * 6 : 0;
	return (
		<div style={{position: 'absolute', inset: 0, transform: `translate(${shake}px, ${shake * 0.7}px)`}}>
			<Paper />
			<Cutout src="strata" x={960} y={820} w={1000} at={106.2 - T} enter="bottom" />
			<Draw d={circlePath(960, 820, 420, 160)} at={108.0 - T} dur={0.8} />
			<Label text="この石こそが" x={500} y={560} at={108.0 - T} tone="white" />
			<Cutout
				src="asteroid"
				x={1800}
				y={60}
				w={260}
				at={106.4 - T}
				move={{to: [1120, 420], from: 106.6 - T, dur: 7, ease: false}}
				scaleTo={{to: 1.9, from: 106.6 - T, dur: 7}}
			/>
			<Stamp text="最大の引き金" x={680} y={230} at={111.8 - T} size={110} />
		</div>
	);
};

// Coordinates on generated maps / backgrounds, tuned after looking at the assets
const MAP_NA_PIN: [number, number] = [849, 553];
const YUCATAN: [number, number] = [980, 660];
const MAMMAL_POS: [number, number] = [875, 776];

const SCENES: {at: number; C: React.FC<{T: number}>}[] = [
	{at: 0, C: S1},
	{at: 9.9, C: S2},
	{at: 16.0, C: S3},
	{at: 24.4, C: S4},
	{at: 34.2, C: S5},
	{at: 43.2, C: S6},
	{at: 49.8, C: S7},
	{at: 60.6, C: S8},
	{at: 64.2, C: S9},
	{at: 72.2, C: S10},
	{at: 83.8, C: S11},
	{at: 93.0, C: S12},
	{at: 106.1, C: S13},
];

// Paper push transition: each scene slides in over the previous one
const SceneShell: React.FC<{children: React.ReactNode; index: number}> = ({children, index}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const s = index === 0 ? 1 : spring({frame, fps, config: {damping: 16, mass: 0.8}});
	const dir = index % 2 === 0 ? 1 : -1;
	const push = 1 + (frame / fps) * 0.004;
	return (
		<AbsoluteFill
			style={{
				transform: `translateX(${(1 - s) * 1920 * dir}px) rotate(${(1 - s) * 3 * dir}deg) scale(${push})`,
				boxShadow: '0 0 60px rgba(0,0,0,0.45)',
				overflow: 'hidden',
			}}
		>
			{children}
		</AbsoluteFill>
	);
};

export const Vox: React.FC = () => {
	const frame = useCurrentFrame();
	const fade = interpolate(frame, [VOX_FRAMES - 36, VOX_FRAMES], [1, 0], {extrapolateLeft: 'clamp'});
	return (
		<AbsoluteFill style={{backgroundColor: '#000'}}>
			<AbsoluteFill style={{opacity: fade}}>
				{SCENES.map(({at, C}, i) => {
					const from = Math.round(at * VOX_FPS);
					const next = i < SCENES.length - 1 ? SCENES[i + 1].at + OVERLAP : END;
					return (
						<Sequence key={at} from={from} durationInFrames={Math.round(next * VOX_FPS) - from}>
							<SceneShell index={i}>
								<C T={at} />
							</SceneShell>
						</Sequence>
					);
				})}
				<AbsoluteFill style={{background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 60%, rgba(30,18,6,0.35) 100%)'}} />
			</AbsoluteFill>
			<Subtitles boxed />
			<Audio src={staticFile('voice.mp3')} />
		</AbsoluteFill>
	);
};
