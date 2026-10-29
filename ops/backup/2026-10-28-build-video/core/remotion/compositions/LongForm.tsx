import React from 'react';
import { AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame } from 'remotion';
import '@fontsource/noto-serif-jp/400.css';
import '@fontsource/noto-serif-jp/700.css';
import { clamp } from '../lib/lib';
import { EpisodeProps, DEFAULT_THEME } from '../types';
import { ThemeCtx, SceneProps } from '../components/common';
import { KenBurns } from '../components/KenBurns';
import { TitleCard } from '../components/TitleCard';
import { Creature } from '../components/Creature';
import { SizeCompare } from '../components/SizeCompare';
import { GeoClock } from '../components/GeoClock';
import { MapDrift } from '../components/MapDrift';
import { Overlay, Caption } from '../components/Overlay';

// Tên component trong scenes.json → component React. Thêm component mới: đăng ký ở đây + enum trong scenes.schema.json
export const COMPONENTS: Record<string, React.FC<SceneProps>> = { KenBurns, TitleCard, Creature, SizeCompare, GeoClock, MapDrift };

const FADE = 12;

const Fader: React.FC<{ children: React.ReactNode; first: boolean }> = ({ children, first }) => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{ opacity: first ? 1 : clamp(f / FADE) }}>{children}</AbsoluteFill>;
};

export const LongForm: React.FC<EpisodeProps> = ({ fps, scenes, theme, audio, grainAsset }) => {
  const th = { ...DEFAULT_THEME, ...theme, palette: { ...DEFAULT_THEME.palette, ...(theme?.palette || {}) } };
  let start = 0;
  return (
    <ThemeCtx.Provider value={th}>
      <AbsoluteFill style={{ background: th.palette.bg }}>
        {audio ? <Audio src={staticFile(audio)} /> : null}
        {scenes.map((s, i) => {
          const from = Math.round(start * fps);
          start += s.duration_s;
          const dur = Math.round(start * fps) - from;
          const C = COMPONENTS[s.component] || KenBurns;
          const lead = i ? FADE : 0;
          return (
            <Sequence key={s.id} from={from - lead} durationInFrames={dur + lead}>
              <Fader first={i === 0}>
                <C dur={dur + lead} asset={s.asset} props={s.props || {}} />
                <Caption text={s.narration} dur={dur + lead} />
              </Fader>
            </Sequence>
          );
        })}
        <Overlay grainAsset={grainAsset} />
      </AbsoluteFill>
    </ThemeCtx.Provider>
  );
};
