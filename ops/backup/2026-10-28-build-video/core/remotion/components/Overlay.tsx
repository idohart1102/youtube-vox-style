import React from 'react';
import { AbsoluteFill, Img, staticFile, useCurrentFrame } from 'remotion';
import { Svg, useTheme } from './common';

// Hạt giấy + vignette theo theme của kênh
export const Overlay: React.FC<{ grainAsset?: string }> = ({ grainAsset }) => {
  const f = useCurrentFrame();
  const t = useTheme();
  return (
    <AbsoluteFill style={{ pointerEvents: 'none' }}>
      {grainAsset && (t.grain ?? 0) > 0 ? (
        <Img src={staticFile(grainAsset)} style={{ position: 'absolute', inset: 0, width: 1920, height: 1080, mixBlendMode: 'multiply', opacity: t.grain, transform: `translate(${(f % 3) - 1}px,${((f >> 1) % 3) - 1}px) scale(1.01)` }} />
      ) : null}
      {(t.vignette ?? 0) > 0 ? (
        <Svg style={{ opacity: Math.min(1, (t.vignette as number) * 1.6) }}>
          <rect width={1920} height={1080} fill="url(#vignette)" />
        </Svg>
      ) : null}
    </AbsoluteFill>
  );
};

// Phụ đề lời đọc của cảnh (theme.subtitles = true)
export const Caption: React.FC<{ text?: string; dur: number }> = ({ text, dur }) => {
  const f = useCurrentFrame();
  const t = useTheme();
  if (!text || t.subtitles === false) return null;
  const o = Math.min(1, f / 8, (dur - f) / 8);
  return (
    <div style={{ position: 'absolute', bottom: 60, left: 160, right: 160, textAlign: 'center', opacity: Math.max(0, o) }}>
      <span style={{ fontFamily: `"${t.font}", serif`, fontSize: 40, lineHeight: 1.5, color: '#fff', fontWeight: 700, background: 'rgba(16,10,6,0.55)', padding: '6px 18px', boxDecorationBreak: 'clone', WebkitBoxDecorationBreak: 'clone' }}>{text}</span>
    </div>
  );
};
