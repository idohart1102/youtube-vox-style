import React from 'react';
import { AbsoluteFill, Img, staticFile, useCurrentFrame } from 'remotion';
import { clamp, ease } from '../lib/lib';
import { assetPath } from '../types';
import { SceneProps, Label, STICKER, enterFx } from './common';

// Cảnh 2.5D kiểu Vox: ảnh nền + các lớp cutout PNG trong suốt, lớp càng gần trôi càng nhanh.
// props: cam ("in" | "out" | "left" | "right", mặc định "in"),
//   layers: [{asset, x, y (điểm giữa-đáy, px), h (chiều cao px), depth (0 xa .. 1 gần, mặc định 0.6),
//             at_s, enter ("pop" | "rise" | "fade"), sticker (mặc định true), flip, drift (px tự trôi ngang)}],
//   label, sub
export const Parallax: React.FC<SceneProps> = ({ dur, asset, props }) => {
  const f = useCurrentFrame();
  const k = ease(clamp(f / dur));
  const cam = props.cam || 'in';
  const zoom = cam === 'in' ? 0.06 * k : cam === 'out' ? 0.06 * (1 - k) : 0.02;
  const pan = cam === 'left' ? 40 - 80 * k : cam === 'right' ? -40 + 80 * k : 0;
  const layers: any[] = props.layers || [];
  return (
    <AbsoluteFill style={{ overflow: 'hidden' }}>
      {asset ? (
        <Img src={staticFile(assetPath(asset))} style={{ position: 'absolute', width: 1920, height: 1080, objectFit: 'cover', transform: `scale(${1.02 + zoom}) translateX(${pan}px)`, filter: props.bg_filter }} />
      ) : null}
      {layers.map((l, i) => {
        const d = l.depth ?? 0.6;
        const s = 1 + zoom * (1 + 2 * d);
        const x = ((l.x ?? 960) - 960) * s + 960 + pan * (1 + 1.5 * d) + (l.drift || 0) * k;
        const y = ((l.y ?? 1000) - 540) * s + 540;
        const [o, sc, dy] = enterFx(f, (l.at_s || 0) * 30, l.enter);
        return (
          <Img
            key={i}
            src={staticFile(assetPath(l.asset))}
            style={{ position: 'absolute', left: x, top: y + dy, height: (l.h || 600) * s, opacity: o, transformOrigin: '50% 100%', transform: `translate(-50%,-100%) scale(${sc}) scaleX(${l.flip ? -1 : 1})`, filter: l.sticker === false ? 'drop-shadow(0 14px 18px rgba(0,0,0,0.45))' : STICKER }}
          />
        );
      })}
      {props.label ? <Label text={props.label} sub={props.sub} from={8} to={dur - 10} /> : null}
    </AbsoluteFill>
  );
};
