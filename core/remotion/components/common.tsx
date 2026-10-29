import React from 'react';
import { spring, useCurrentFrame } from 'remotion';
import { Defs, ramp } from '../lib/lib';
import { Theme, DEFAULT_THEME } from '../types';

export const ThemeCtx = React.createContext<Theme>(DEFAULT_THEME);
export const useTheme = () => React.useContext(ThemeCtx);
export const fontOf = (t: Theme) => `"${t.font}", "Be Vietnam Pro", "Noto Serif JP", sans-serif`;

// Chữ cố định theo ngôn ngữ kênh (theme.lang)
const STR: Record<string, Record<string, string>> = {
  vi: { clock: 'LỊCH TRÁI ĐẤT · 4,6 TỶ NĂM = 24 GIỜ', 'xac-nhan': 'Đã xác nhận', 'co-the': 'Có thể', 'tranh-cai': 'Còn tranh cãi', recon: 'Tái hiện', hoangsa: 'Quần đảo Hoàng Sa', truongsa: 'Quần đảo Trường Sa', biendong: 'Biển Đông' },
  ja: { clock: '地球カレンダー（46億年＝24時間）', 'xac-nhan': '確認済み', 'co-the': '可能性', 'tranh-cai': '議論中', recon: '再現', hoangsa: 'ホアンサ諸島', truongsa: 'チュオンサ諸島', biendong: '東海' },
};
export const tr = (t: Theme, k: string) => (STR[t.lang || 'ja'] || STR.ja)[k] || k;
const viNum = (x: number, d = 0) => x.toLocaleString('de-DE', { maximumFractionDigits: d });
export const agoText = (t: Theme, ma: number) =>
  t.lang === 'vi'
    ? ma >= 1000 ? `${viNum(ma / 1000, 1)} tỷ năm trước` : ma >= 1 ? `${viNum(Math.round(ma))} triệu năm trước` : `${viNum(Math.round(ma * 1e6 / 100) * 100)} năm trước`
    : jaAgo(ma);
const SHADOW = '3px 3px 0 #1c140e, 0 0 18px rgba(0,0,0,0.6)';

// Mọi component nhận cùng một bộ props cơ bản
export type SceneProps = { dur: number; asset?: string; props: Record<string, any> };

export const Svg: React.FC<{ children: React.ReactNode; style?: React.CSSProperties }> = ({ children, style }) => (
  <svg viewBox="0 0 1920 1080" width={1920} height={1080} style={{ position: 'absolute', inset: 0, ...style }}>
    <Defs />
    {children}
  </svg>
);

export const fade = (f: number, from: number, to: number, len = 18) => ramp(f, from, from + len) * (1 - ramp(f, to - len, to));

export const Label: React.FC<{ text: string; sub?: string; from: number; to: number }> = ({ text, sub, from, to }) => {
  const f = useCurrentFrame();
  const t = useTheme();
  const o = fade(f, from, to);
  if (o <= 0) return null;
  return (
    <div style={{ position: 'absolute', left: 90, top: 90, opacity: o, transform: `translateX(${(1 - o) * -30}px)`, fontFamily: fontOf(t) }}>
      <div style={{ width: 70, height: 4, background: t.palette.accent, marginBottom: 14, boxShadow: '2px 2px 0 #1c140e' }} />
      <div style={{ fontSize: 54, color: t.palette.fg, fontWeight: 700, letterSpacing: 4, textShadow: SHADOW }}>{text}</div>
      {sub ? <div style={{ fontSize: 30, color: t.palette.fg, opacity: 0.85, marginTop: 8, letterSpacing: 3, textShadow: SHADOW }}>{sub}</div> : null}
    </div>
  );
};

export const BigText: React.FC<{ text: string; from: number; to: number; y?: number; size?: number; color?: string }> = ({ text, from, to, y = 380, size = 110, color }) => {
  const f = useCurrentFrame();
  const t = useTheme();
  const o = fade(f, from, to, 20);
  if (o <= 0) return null;
  return (
    <div style={{ position: 'absolute', top: y, width: '100%', textAlign: 'center', fontFamily: fontOf(t), fontWeight: 700, fontSize: size, color: color || t.palette.fg, letterSpacing: 10, opacity: o, transform: `scale(${0.96 + o * 0.04})`, textShadow: '4px 4px 0 #1c140e, 0 0 40px rgba(0,0,0,0.7)' }}>
      {text}
    </div>
  );
};

// Định dạng thời gian địa chất theo kiểu Nhật: 252 Ma → 2.5億年前, 66 Ma → 6600万年前
export const jaAgo = (ma: number) =>
  ma >= 100 ? `${(ma / 100).toFixed(ma % 100 === 0 ? 0 : 1)}億年前` : ma >= 0.01 ? `${Math.round(ma * 100)}万年前` : `${Math.round(ma * 1e6)}年前`;

// Viền trắng kiểu sticker + bóng đổ cho ảnh cutout PNG trong suốt (chất Vox)
export const STICKER = 'drop-shadow(4px 0 0 #fff) drop-shadow(-4px 0 0 #fff) drop-shadow(0 4px 0 #fff) drop-shadow(0 -4px 0 #fff) drop-shadow(0 14px 18px rgba(0,0,0,0.45))';

// Hiệu ứng xuất hiện của 1 lớp: pop (phóng nhẹ), rise (trồi lên), fade. Trả về [opacity, scale, dy]
// pop và rise dùng spring "crisp": vượt nhẹ rồi dừng gọn, không nảy nhiều lần
export const enterFx = (f: number, at: number, kind = 'pop'): [number, number, number] => {
  const k = ramp(f, at, at + 14);
  if (kind === 'fade') return [k, 1, 0];
  const s = spring({ frame: Math.max(0, f - at), fps: 30, config: { damping: 13, stiffness: 160, mass: 0.7 } });
  if (kind === 'rise') return [k, 1, (1 - s) * 80];
  return [k, 0.86 + 0.14 * s, 0];
};

// Chuyển động lặp nhẹ cho cutout (không cần rig): breathe, sway, bob, walk. Gốc xoay/co giãn là chân lớp.
// Trả về chuỗi transform ghép sau translate của lớp.
export const idleFx = (f: number, kind?: string, seed = 0): string => {
  const w = (period_s: number) => (2 * Math.PI * f) / (30 * period_s) + seed * 1.7;
  if (kind === 'breathe') return `scaleY(${1 + 0.015 * Math.sin(w(3.5))})`;
  if (kind === 'sway') return `rotate(${1.5 * Math.sin(w(4))}deg)`;
  if (kind === 'bob') return `translateY(${6 * Math.sin(w(2.5))}px)`;
  if (kind === 'walk') return `translateY(${-3 * Math.abs(Math.sin(w(1.1)))}px)`;
  return '';
};

// Rung máy khi va chạm: tắt dần trong len khung, biên độ amp px. Trả về [dx, dy]
export const shakeXY = (f: number, at: number, len: number, amp = 14): [number, number] => {
  const t = f - at;
  if (t < 0 || t > len) return [0, 0];
  const e = (amp * (1 - t / len)) / 1.5;
  return [e * (Math.sin(t * 1.9) + 0.5 * Math.sin(t * 4.3 + 1)), e * (Math.sin(t * 2.3 + 2) + 0.5 * Math.sin(t * 3.7))];
};

// Asset ẩn cho câu hỏi: không lộ đáp án trước khi lời đọc trả lời.
// hide: silhouette (bóng đen viền trắng) | fog (mờ tối) | blur (nhòe mạnh) | keyhole (chỉ lộ 1 vòng nhỏ).
// unmask_s: giây (tính từ đầu cảnh) bắt đầu lộ ra trong 0,8 giây; không có thì ẩn suốt cảnh.
export const hiddenAmount = (f: number, hide?: string, unmask_s?: number) =>
  !hide ? 0 : unmask_s == null ? 1 : 1 - ramp(f, unmask_s * 30, unmask_s * 30 + 24);

export const hideFx = (hide: string | undefined, h: number): { filter: string; clipPath?: string; opacity: number } => {
  if (!hide || h <= 0) return { filter: '', opacity: 1 };
  if (hide === 'silhouette') return { filter: `brightness(${1 - h})`, opacity: 1 };
  if (hide === 'fog') return { filter: `blur(${12 * h}px) brightness(${1 - 0.45 * h})`, opacity: 1 - 0.35 * h };
  if (hide === 'keyhole') return { filter: '', clipPath: `circle(${22 + 60 * (1 - h)}% at 50% 45%)`, opacity: 1 };
  return { filter: `blur(${22 * h}px)`, opacity: 1 };
};
