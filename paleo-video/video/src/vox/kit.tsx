import React from 'react';
import {AbsoluteFill, Img, interpolate, random, spring, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {loadFont} from '@remotion/google-fonts/NotoSansJP';

export const {fontFamily: sans} = loadFont('normal', {weights: ['900'], ignoreTooManyRequestsWarning: true});

export const RED = '#d6322b';
export const YELLOW = '#f6d743';
export const INK = '#1d1a16';

const asset = (name: string) => staticFile(`vox/${name}.png`);

// Seconds since the enclosing Sequence started
export const useSec = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	return frame / fps;
};

const useEnter = (at: number, damping = 11) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const f = frame - at * fps;
	return {f, s: f < 0 ? 0 : spring({frame: f, fps, config: {damping, mass: 0.7}})};
};

// Stepped jitter at ~7.5 fps gives the hand-animated "boil" of cut paper
const useBoil = (seed: string, amount: number) => {
	const frame = useCurrentFrame();
	const step = Math.floor(frame / 4);
	return (random(`${seed}-${step}`) - 0.5) * amount;
};

type Enter = 'pop' | 'left' | 'right' | 'bottom' | 'top';

const enterTransform = (enter: Enter, s: number) => {
	switch (enter) {
		case 'left':
			return `translateX(${(1 - s) * -1500}px) rotate(${(1 - s) * -8}deg)`;
		case 'right':
			return `translateX(${(1 - s) * 1500}px) rotate(${(1 - s) * 8}deg)`;
		case 'bottom':
			return `translateY(${(1 - s) * 900}px)`;
		case 'top':
			return `translateY(${(1 - s) * -900}px)`;
		default:
			return `scale(${s}) rotate(${(1 - s) * -14}deg)`;
	}
};

type Move = {to: [number, number]; from: number; dur: number; ease?: boolean};

const useMove = (x: number, y: number, move?: Move) => {
	const t = useSec();
	if (!move) return [x, y, 0] as const;
	const p = interpolate(t, [move.from, move.from + move.dur], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
		easing: move.ease === false ? undefined : Easing.inOut(Easing.cubic),
	});
	return [x + (move.to[0] - x) * p, y + (move.to[1] - y) * p, p] as const;
};

export const Cutout: React.FC<{
	src: string;
	x: number;
	y: number;
	w: number;
	at: number;
	enter?: Enter;
	rot?: number;
	flip?: boolean;
	move?: Move;
	bob?: number;
	tremble?: number;
	scaleTo?: {to: number; from: number; dur: number};
	dimAt?: number;
	style?: React.CSSProperties;
}> = ({src, x, y, w, at, enter = 'pop', rot = 0, flip, move, bob, tremble, scaleTo, dimAt, style}) => {
	const {s} = useEnter(at);
	const t = useSec();
	const boil = useBoil(src + x, 1.4);
	const [cx, cy, p] = useMove(x, y, move);
	if (t < at) return null;
	const bobY = bob && move && p > 0 && p < 1 ? -Math.abs(Math.sin(t * 7)) * bob : 0;
	const shake = tremble && t > tremble ? Math.sin(t * 90) * 3 : 0;
	const grow = scaleTo
		? interpolate(t, [scaleTo.from, scaleTo.from + scaleTo.dur], [1, scaleTo.to], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.in(Easing.quad)})
		: 1;
	const dim = dimAt !== undefined ? interpolate(t, [dimAt, dimAt + 0.6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;
	return (
		<div
			style={{
				position: 'absolute',
				left: cx - w / 2 + shake,
				top: cy + bobY,
				width: w,
				transform: `translateY(-50%) ${enterTransform(enter, s)} rotate(${rot + boil + dim * 12}deg) scale(${grow})`,
				filter: `drop-shadow(8px 12px 0 rgba(40,25,10,0.28)) grayscale(${dim}) brightness(${1 - dim * 0.35})`,
				...style,
			}}
		>
			<Img src={asset(src)} style={{width: '100%', transform: flip ? 'scaleX(-1)' : undefined}} />
		</div>
	);
};

const tornPolygon = (seed: string) => {
	const pts: string[] = [];
	const n = 26;
	const j = (k: string) => random(`${seed}-${k}`) * 1.6;
	for (let i = 0; i <= n; i++) pts.push(`${(i / n) * 100}% ${j(`t${i}`)}%`);
	for (let i = 0; i <= n; i++) pts.push(`${100 - j(`r${i}`)}% ${(i / n) * 100}%`);
	for (let i = n; i >= 0; i--) pts.push(`${(i / n) * 100}% ${100 - j(`b${i}`)}%`);
	for (let i = n; i >= 0; i--) pts.push(`${j(`l${i}`)}% ${(i / n) * 100}%`);
	return `polygon(${pts.join(',')})`;
};

// Background painting presented as a torn paper card
export const Card: React.FC<{
	src: string;
	x: number;
	y: number;
	w: number;
	at: number;
	enter?: Enter;
	rot?: number;
	push?: number;
	objPos?: string;
	style?: React.CSSProperties;
}> = ({src, x, y, w, at, enter = 'right', rot = 0, push = 0.06, objPos, style}) => {
	const {s} = useEnter(at, 14);
	const t = useSec();
	if (t < at) return null;
	const h = (w * 2) / 3;
	return (
		<div
			style={{
				position: 'absolute',
				left: x - w / 2,
				top: y - h / 2,
				width: w,
				height: h,
				transform: `${enterTransform(enter, s)} rotate(${rot}deg)`,
				filter: 'drop-shadow(10px 14px 0 rgba(40,25,10,0.3))',
				...style,
			}}
		>
			<div style={{width: '100%', height: '100%', overflow: 'hidden', clipPath: tornPolygon(src), background: '#f3ead6'}}>
				<Img
					src={asset(src)}
					style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: objPos, transform: `scale(${1 + push * Math.min(1, (t - at) / 8)})`}}
				/>
			</div>
		</div>
	);
};

export const Paper: React.FC = () => (
	<AbsoluteFill>
		<Img src={asset('paper')} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
	</AbsoluteFill>
);

export const Label: React.FC<{
	text: string;
	x: number;
	y: number;
	at: number;
	size?: number;
	tone?: 'yellow' | 'white' | 'red';
	rot?: number;
	until?: number;
}> = ({text, x, y, at, size = 54, tone = 'yellow', rot = -1.5, until}) => {
	const {f, s} = useEnter(at, 13);
	const t = useSec();
	if (t < at || (until !== undefined && t > until)) return null;
	const swipe = interpolate(f, [0, 8], [0, 1], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
	const bg = tone === 'yellow' ? YELLOW : tone === 'red' ? RED : '#fffaf0';
	return (
		<div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%, -50%) rotate(${rot}deg) scale(${0.85 + 0.15 * s})`}}>
			<div style={{position: 'relative', padding: '8px 22px'}}>
				<div
					style={{
						position: 'absolute',
						inset: 0,
						background: bg,
						transformOrigin: 'left center',
						transform: `scaleX(${swipe})`,
						boxShadow: '5px 6px 0 rgba(40,25,10,0.25)',
					}}
				/>
				<div
					style={{
						position: 'relative',
						fontFamily: sans,
						fontWeight: 900,
						fontSize: size,
						color: tone === 'red' ? '#fff' : INK,
						whiteSpace: 'nowrap',
						opacity: interpolate(f, [3, 8], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
					}}
				>
					{text}
				</div>
			</div>
		</div>
	);
};

export const Stamp: React.FC<{text: string; x: number; y: number; at: number; size?: number; rot?: number}> = ({text, x, y, at, size = 120, rot = -8}) => {
	const {f} = useEnter(at);
	const t = useSec();
	if (t < at) return null;
	const k = interpolate(f, [0, 6], [2.4, 1], {extrapolateRight: 'clamp', easing: Easing.in(Easing.quad)});
	return (
		<div
			style={{
				position: 'absolute',
				left: x,
				top: y,
				transform: `translate(-50%, -50%) rotate(${rot}deg) scale(${k})`,
				opacity: interpolate(f, [0, 4], [0, 0.92], {extrapolateRight: 'clamp'}),
				border: `10px solid ${RED}`,
				borderRadius: 14,
				padding: '4px 30px',
				fontFamily: sans,
				fontWeight: 900,
				fontSize: size,
				color: RED,
				whiteSpace: 'nowrap',
				mixBlendMode: 'multiply',
			}}
		>
			{text}
		</div>
	);
};

// Hand-drawn stroke revealed along its length
export const Draw: React.FC<{d: string; at: number; dur?: number; color?: string; width?: number; dashed?: boolean; arrow?: boolean}> = ({
	d,
	at,
	dur = 0.8,
	color = RED,
	width = 10,
	dashed,
	arrow,
}) => {
	const t = useSec();
	if (t < at) return null;
	const p = interpolate(t, [at, at + dur], [0, 1], {extrapolateRight: 'clamp', easing: Easing.out(Easing.quad)});
	const id = `m${Math.round(random(d) * 1e9)}`;
	return (
		<svg width={1920} height={1080} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
			<defs>
				<mask id={id} maskUnits="userSpaceOnUse">
					<path d={d} pathLength={1} stroke="#fff" strokeWidth={width + 8} fill="none" strokeDasharray="1 1" strokeDashoffset={1 - p} strokeLinecap="round" />
				</mask>
				<marker id={`${id}a`} viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
					<path d="M0,0 L10,5 L0,10 z" fill={color} />
				</marker>
			</defs>
			<path
				d={d}
				stroke={color}
				strokeWidth={width}
				fill="none"
				strokeLinecap="round"
				strokeLinejoin="round"
				strokeDasharray={dashed ? `${width * 2.2} ${width * 2}` : undefined}
				mask={`url(#${id})`}
			/>
			{arrow && p > 0.97 ? <path d={d} stroke={color} strokeOpacity={0} strokeWidth={width} fill="none" markerEnd={`url(#${id}a)`} /> : null}
		</svg>
	);
};

export const circlePath = (cx: number, cy: number, rx: number, ry: number) => {
	const pts: string[] = [];
	for (let i = 0; i <= 40; i++) {
		const a = -Math.PI / 2 + (i / 36) * Math.PI * 2;
		const wob = 1 + (i / 40) * 0.08;
		pts.push(`${(cx + Math.cos(a) * rx * wob).toFixed(1)},${(cy + Math.sin(a) * ry * wob).toFixed(1)}`);
	}
	return `M${pts.join(' L')}`;
};

export const Counter: React.FC<{to: number; at: number; dur?: number; x: number; y: number; suffix: string; size?: number}> = ({
	to,
	at,
	dur = 1.2,
	x,
	y,
	suffix,
	size = 120,
}) => {
	const t = useSec();
	const {s} = useEnter(at);
	if (t < at) return null;
	const v = Math.round(interpolate(t, [at, at + dur], [0, to], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)}));
	return (
		<div
			style={{
				position: 'absolute',
				left: x,
				top: y,
				transform: `translate(-50%, -50%) scale(${s})`,
				fontFamily: sans,
				fontWeight: 900,
				fontSize: size,
				color: INK,
				whiteSpace: 'nowrap',
				textShadow: '6px 6px 0 rgba(246,215,67,0.9)',
			}}
		>
			{v.toLocaleString('ja-JP')}
			<span style={{fontSize: size * 0.5}}>{suffix}</span>
		</div>
	);
};

export const Clock: React.FC<{x: number; y: number; r: number; at: number; spinFrom: number; spinDur: number}> = ({x, y, r, at, spinFrom, spinDur}) => {
	const t = useSec();
	const {s} = useEnter(at);
	if (t < at) return null;
	const spin = interpolate(t, [spinFrom, spinFrom + spinDur], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const minute = spin * 360 * 12;
	const hour = spin * 360;
	return (
		<svg
			width={r * 2 + 20}
			height={r * 2 + 20}
			style={{position: 'absolute', left: x - r - 10, top: y - r - 10, transform: `scale(${s})`, filter: 'drop-shadow(6px 8px 0 rgba(40,25,10,0.28))'}}
		>
			<g transform={`translate(${r + 10},${r + 10})`}>
				<circle r={r} fill="#fffaf0" stroke={INK} strokeWidth={10} />
				{new Array(12).fill(0).map((_, i) => (
					<line key={i} x1={0} y1={-r + 14} x2={0} y2={-r + 34} stroke={INK} strokeWidth={6} transform={`rotate(${i * 30})`} />
				))}
				<line x1={0} y1={0} x2={0} y2={-r * 0.5} stroke={INK} strokeWidth={12} strokeLinecap="round" transform={`rotate(${hour})`} />
				<line x1={0} y1={0} x2={0} y2={-r * 0.78} stroke={RED} strokeWidth={8} strokeLinecap="round" transform={`rotate(${minute})`} />
				<circle r={10} fill={INK} />
			</g>
		</svg>
	);
};

export const Pin: React.FC<{x: number; y: number; at: number}> = ({x, y, at}) => {
	const {s} = useEnter(at, 9);
	const t = useSec();
	if (t < at) return null;
	return (
		<svg width={70} height={100} style={{position: 'absolute', left: x - 35, top: y - 95 - (1 - s) * 300, filter: 'drop-shadow(4px 6px 0 rgba(40,25,10,0.3))'}}>
			<path d="M35,96 C35,96 6,56 6,34 A29,29 0 1 1 64,34 C64,56 35,96 35,96 Z" fill={RED} stroke="#fff" strokeWidth={4} />
			<circle cx={35} cy={34} r={11} fill="#fff" />
		</svg>
	);
};
