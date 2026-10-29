import React from 'react';
import { AbsoluteFill, Img, staticFile, useCurrentFrame } from 'remotion';
import { clamp } from '../lib/lib';
import { assetPath } from '../types';
import { SceneProps, Label, STICKER, enterFx, useTheme, fontOf } from './common';

// Cắt dán kiểu Vox, tối đa 3 mảnh. Nền: asset (làm tối) hoặc màu nền kênh.
// props: items: [{asset, x, y (tâm, px), w (rộng px), rot (độ), at_s, photo (true = ảnh thật: viền trắng + credit), credit}], label, sub
export const Collage: React.FC<SceneProps> = ({ dur, asset, props }) => {
  const f = useCurrentFrame();
  const t = useTheme();
  const k = clamp(f / dur);
  const items: any[] = (props.items || []).slice(0, 3);
  return (
    <AbsoluteFill style={{ background: t.palette.bg, overflow: 'hidden' }}>
      {asset ? <Img src={staticFile(assetPath(asset))} style={{ position: 'absolute', width: 1920, height: 1080, objectFit: 'cover', filter: 'brightness(0.45) blur(2px)', transform: `scale(${1.04 + 0.03 * k})` }} /> : null}
      <AbsoluteFill style={{ transform: `scale(${1 + 0.04 * k})` }}>
        {items.map((it, i) => {
          const [o, sc, dy] = enterFx(f, (it.at_s ?? i * 0.6) * 30, it.enter);
          const rot = (it.rot ?? [-4, 3, -2][i]) * (0.6 + 0.4 * o);
          return (
            <div key={i} style={{ position: 'absolute', left: it.x ?? 960, top: (it.y ?? 540) + dy, width: it.w || 700, opacity: o, transform: `translate(-50%,-50%) rotate(${rot}deg) scale(${sc})` }}>
              <Img
                src={staticFile(assetPath(it.asset))}
                style={it.photo
                  ? { width: '100%', display: 'block', border: '12px solid #f4efe6', boxShadow: '0 16px 36px rgba(0,0,0,0.55)' }
                  : { width: '100%', display: 'block', filter: STICKER }}
              />
              {it.photo && it.credit ? <div style={{ marginTop: 8, fontFamily: fontOf(t), fontSize: 18, color: t.palette.fg, opacity: 0.8 }}>{it.credit}</div> : null}
            </div>
          );
        })}
      </AbsoluteFill>
      {props.label ? <Label text={props.label} sub={props.sub} from={8} to={dur - 10} /> : null}
    </AbsoluteFill>
  );
};
