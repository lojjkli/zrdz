import React from 'react';
import {interpolate} from 'remotion';
import {CHAT, ChatLine, diamondsAt, TAPS, VOICE_CUES, speakerOf, voiceSec, voiceText} from '../timeline';

export const UI_FONT = '"Source Sans 3", "Noto Color Emoji", sans-serif';
export const GAME_FONT = '"Fredoka", "Noto Color Emoji", sans-serif';
export const DOC_FONT = '"Bebas Neue", sans-serif';

const fmt = (n: number) => n.toLocaleString('en-US');

// ---------------------------------------------------------------- icons
export const RobloxLogo: React.FC<{size?: number; color?: string}> = ({size = 30, color = '#fff'}) => (
	<svg width={size} height={size} viewBox="0 0 100 100">
		<g transform="rotate(15 50 50)">
			<rect x="12" y="12" width="76" height="76" rx="8" fill={color} />
			<rect x="40" y="40" width="20" height="20" fill="#000" opacity={0.85} />
		</g>
	</svg>
);

const ChatIcon: React.FC = () => (
	<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2" strokeLinejoin="round">
		<path d="M4 5h16v11H9l-5 4z" />
	</svg>
);

export const MicIcon: React.FC<{active?: boolean; level?: number; size?: number}> = ({active, level = 0, size = 34}) => (
	<svg width={size} height={size} viewBox="0 0 24 24">
		<defs>
			<clipPath id="micclip">
				<rect x="8" y={4 + 11 * (1 - level)} width="8" height={11 * level + 1} />
			</clipPath>
		</defs>
		<rect x="8" y="3" width="8" height="13" rx="4" fill="none" stroke="#fff" strokeWidth="2" />
		{active ? <rect x="8" y="3" width="8" height="13" rx="4" fill="#00e676" clipPath="url(#micclip)" /> : null}
		<path d="M5 11a7 7 0 0 0 14 0M12 18v3" fill="none" stroke="#fff" strokeWidth="2" strokeLinecap="round" />
	</svg>
);

export const DiamondIcon: React.FC<{size?: number}> = ({size = 44}) => (
	<svg width={size} height={size} viewBox="0 0 64 64">
		<polygon points="14,22 24,10 40,10 50,22 32,56" fill="#33d6ff" stroke="#0b3a5c" strokeWidth="4" strokeLinejoin="round" />
		<polygon points="14,22 50,22 32,56" fill="#18a8e6" />
		<polygon points="24,10 32,22 40,10" fill="#a6f2ff" />
		<polygon points="14,22 24,10 32,22" fill="#7ee8ff" />
		<polygon points="14,22 24,10 40,10 50,22 32,56" fill="none" stroke="#0b3a5c" strokeWidth="4" strokeLinejoin="round" />
	</svg>
);

export const CoinIcon: React.FC<{size?: number}> = ({size = 40}) => (
	<svg width={size} height={size} viewBox="0 0 64 64">
		<circle cx="32" cy="32" r="26" fill="#ffc93c" stroke="#7a4a00" strokeWidth="4" />
		<circle cx="32" cy="32" r="17" fill="none" stroke="#e8a400" strokeWidth="4" />
	</svg>
);

export const RobuxIcon: React.FC<{size?: number; color?: string}> = ({size = 26, color = '#fff'}) => (
	<svg width={size} height={size} viewBox="0 0 24 24">
		<path d="M12 2l8.66 5v10L12 22l-8.66-5V7z" fill="none" stroke={color} strokeWidth="2.4" />
		<rect x="9" y="9" width="6" height="6" fill="none" stroke={color} strokeWidth="2.4" />
	</svg>
);

// ---------------------------------------------------------------- roblox core gui
export const TopBar: React.FC<{talking: boolean; t: number}> = ({talking, t}) => {
	const level = talking ? 0.35 + 0.65 * Math.abs(Math.sin(t * 17) * Math.sin(t * 5.3)) : 0;
	const btn: React.CSSProperties = {
		width: 64,
		height: 64,
		borderRadius: 18,
		background: 'rgba(18,18,21,0.62)',
		display: 'flex',
		alignItems: 'center',
		justifyContent: 'center',
	};
	return (
		<div style={{position: 'absolute', left: 24, top: 22, display: 'flex', gap: 12}}>
			<div style={btn}>
				<RobloxLogo />
			</div>
			<div style={btn}>
				<ChatIcon />
			</div>
			<div style={{...btn, background: talking ? 'rgba(18,18,21,0.75)' : btn.background}}>
				<MicIcon active={talking} level={level} />
			</div>
		</div>
	);
};

export const ChatWindow: React.FC<{t: number; lines?: ChatLine[]; from?: number}> = ({t, lines = CHAT, from = 0}) => {
	const visible = lines.filter((l) => l.at <= t && l.at >= from).slice(-7);
	return (
		<div
			style={{
				position: 'absolute',
				left: 24,
				top: 100,
				width: 600,
				height: 300,
				borderRadius: 14,
				background: 'rgba(0,0,0,0.30)',
				overflow: 'hidden',
				display: 'flex',
				flexDirection: 'column',
				justifyContent: 'flex-end',
				padding: '10px 16px 56px',
				boxSizing: 'border-box',
				fontFamily: UI_FONT,
			}}
		>
			{visible.map((l) => {
				const k = Math.min(1, (t - l.at) / 0.18);
				return (
					<div
						key={l.at + l.text}
						style={{
							fontSize: 27,
							lineHeight: '34px',
							fontWeight: 600,
							color: l.system ? '#d7d7d7' : '#fff',
							opacity: k,
							transform: `translateY(${(1 - k) * 10}px)`,
							textShadow: '0 1px 2px rgba(0,0,0,0.9)',
							whiteSpace: 'nowrap',
						}}
					>
						{l.system ? (
							<span style={{fontStyle: 'italic'}}>{l.text}</span>
						) : (
							<>
								<span style={{color: l.color, fontWeight: 700}}>{l.name}: </span>
								{l.text}
							</>
						)}
					</div>
				);
			})}
			<div
				style={{
					position: 'absolute',
					left: 10,
					right: 10,
					bottom: 10,
					height: 38,
					borderRadius: 10,
					background: 'rgba(0,0,0,0.35)',
					color: 'rgba(255,255,255,0.55)',
					fontSize: 21,
					lineHeight: '38px',
					paddingLeft: 14,
				}}
			>
				Tap here to chat
			</div>
		</div>
	);
};

export const Thumbstick: React.FC<{x?: number; y?: number; opacity?: number}> = ({x = 0, y = 0, opacity = 1}) => (
	<div style={{position: 'absolute', left: 120, top: 700, width: 230, height: 230, opacity}}>
		<div
			style={{
				position: 'absolute',
				inset: 0,
				borderRadius: '50%',
				background: 'rgba(0,0,0,0.22)',
				border: '4px solid rgba(255,255,255,0.35)',
			}}
		/>
		<div
			style={{
				position: 'absolute',
				left: 115 - 48 + x * 62,
				top: 115 - 48 + y * 62,
				width: 96,
				height: 96,
				borderRadius: '50%',
				background: 'rgba(255,255,255,0.42)',
				boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
			}}
		/>
	</div>
);

export const JumpButton: React.FC<{pressed?: boolean}> = ({pressed}) => (
	<div
		style={{
			position: 'absolute',
			right: 110,
			top: 760,
			width: 150,
			height: 150,
			borderRadius: '50%',
			background: pressed ? 'rgba(255,255,255,0.35)' : 'rgba(0,0,0,0.22)',
			border: '4px solid rgba(255,255,255,0.4)',
			display: 'flex',
			alignItems: 'center',
			justifyContent: 'center',
		}}
	>
		<svg width="70" height="70" viewBox="0 0 24 24">
			<path d="M5 15l7-7 7 7" fill="none" stroke="rgba(255,255,255,0.85)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
		</svg>
	</div>
);

// ---------------------------------------------------------------- pet sim style HUD
const outlined: React.CSSProperties = {
	fontFamily: GAME_FONT,
	fontWeight: 700,
	color: '#fff',
	WebkitTextStroke: '7px #1a1a2e',
	paintOrder: 'stroke fill',
};

export const Currency: React.FC<{t: number; coins?: number}> = ({t, coins = 48210000}) => {
	const d = diamondsAt(t);
	const since = t - d.changedAt;
	const pulse = since < 0.5 ? 1 + 0.18 * Math.sin((since / 0.5) * Math.PI) : 1;
	const flash = since < 0.8 && d.delta < 0 ? '#ff5757' : since < 0.8 && d.delta > 0 ? '#7dff8a' : '#fff';
	const broke = d.value === 0;
	const pill: React.CSSProperties = {
		display: 'flex',
		alignItems: 'center',
		gap: 12,
		height: 64,
		padding: '0 22px 0 12px',
		borderRadius: 20,
		background: 'linear-gradient(180deg, rgba(40,40,70,0.85), rgba(20,20,40,0.85))',
		border: '4px solid #1a1a2e',
		boxShadow: '0 4px 0 rgba(0,0,0,0.35)',
		minWidth: 300,
	};
	return (
		<div style={{position: 'absolute', right: 28, top: 24, display: 'flex', flexDirection: 'column', gap: 12, alignItems: 'flex-end'}}>
			<div style={{...pill, transform: `scale(${pulse})`, transformOrigin: 'right center'}}>
				<DiamondIcon />
				<div style={{...outlined, fontSize: 40, color: broke ? '#ff5757' : flash}}>{fmt(d.value)}</div>
				<div
					style={{
						marginLeft: 'auto',
						width: 40,
						height: 40,
						borderRadius: 12,
						background: '#36d96b',
						border: '3px solid #1a1a2e',
						...outlined,
						WebkitTextStroke: '4px #1a1a2e',
						fontSize: 34,
						lineHeight: '36px',
						textAlign: 'center',
					}}
				>
					+
				</div>
			</div>
			<div style={pill}>
				<CoinIcon />
				<div style={{...outlined, fontSize: 36}}>{fmt(coins)}</div>
			</div>
			{since < 1.4 && d.delta !== 0 ? (
				<div
					style={{
						...outlined,
						fontSize: 42,
						color: d.delta < 0 ? '#ff5757' : '#7dff8a',
						opacity: interpolate(since, [0, 0.2, 1.1, 1.4], [0, 1, 1, 0]),
						transform: `translateY(${-since * 30}px)`,
						marginRight: 16,
					}}
				>
					{d.delta > 0 ? '+' : '-'}
					{fmt(Math.abs(d.delta))}
				</div>
			) : null}
		</div>
	);
};

const MenuButton: React.FC<{label: string; bg: string; icon: string}> = ({label, bg, icon}) => (
	<div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2}}>
		<div
			style={{
				width: 88,
				height: 88,
				borderRadius: 22,
				background: bg,
				border: '4px solid #1a1a2e',
				boxShadow: 'inset 0 -8px 0 rgba(0,0,0,0.2), 0 4px 0 rgba(0,0,0,0.35)',
				display: 'flex',
				alignItems: 'center',
				justifyContent: 'center',
				fontSize: 46,
			}}
		>
			<span style={{fontFamily: '"Noto Color Emoji"'}}>{icon}</span>
		</div>
		<div style={{...outlined, WebkitTextStroke: '5px #1a1a2e', fontSize: 22}}>{label}</div>
	</div>
);

export const SideMenu: React.FC = () => (
	<div style={{position: 'absolute', right: 30, top: 250, display: 'flex', flexDirection: 'column', gap: 14}}>
		<MenuButton label="Pets" bg="linear-gradient(#ffb347,#ff8c1a)" icon="🐾" />
		<MenuButton label="Shop" bg="linear-gradient(#7ee081,#2fb344)" icon="🛒" />
		<MenuButton label="Trade" bg="linear-gradient(#7fc8ff,#2f8ce0)" icon="🤝" />
	</div>
);

export const ZoneBanner: React.FC<{text: string; t: number; from: number}> = ({text, t, from}) => {
	const k = t - from;
	if (k < 0 || k > 3.2) return null;
	const o = interpolate(k, [0, 0.3, 2.6, 3.2], [0, 1, 1, 0]);
	return (
		<div style={{position: 'absolute', top: 130, left: 0, right: 0, textAlign: 'center', opacity: o, transform: `scale(${0.9 + 0.1 * Math.min(1, k * 4)})`}}>
			<div style={{...outlined, fontSize: 64, WebkitTextStroke: '10px #1a1a2e'}}>{text}</div>
		</div>
	);
};

// ---------------------------------------------------------------- billboards (positioned from 3D)
export const Nametag: React.FC<{x: number; y: number; name: string; scale?: number}> = ({x, y, name, scale = 1}) => (
	<div
		style={{
			position: 'absolute',
			left: x,
			top: y,
			transform: `translate(-50%, -100%) scale(${scale})`,
			transformOrigin: 'bottom center',
			fontFamily: UI_FONT,
			fontWeight: 700,
			fontSize: 30,
			color: '#fff',
			textShadow: '0 0 3px #000, 0 0 3px #000, 0 2px 2px #000',
			whiteSpace: 'nowrap',
		}}
	>
		{name}
	</div>
);

export const VoiceBubble: React.FC<{x: number; y: number; t: number; scale?: number}> = ({x, y, t, scale = 1}) => {
	const bars = [0, 1, 2].map((i) => 0.35 + 0.65 * Math.abs(Math.sin(t * (11 + i * 3.7) + i)));
	return (
		<div
			style={{
				position: 'absolute',
				left: x,
				top: y,
				transform: `translate(-50%, -100%) scale(${scale})`,
				transformOrigin: 'bottom center',
				height: 52,
				padding: '0 16px',
				borderRadius: 26,
				background: 'rgba(255,255,255,0.95)',
				display: 'flex',
				alignItems: 'center',
				gap: 6,
				boxShadow: '0 2px 6px rgba(0,0,0,0.3)',
			}}
		>
			<svg width="26" height="26" viewBox="0 0 24 24">
				<rect x="8" y="3" width="8" height="13" rx="4" fill="#111" />
				<path d="M5 11a7 7 0 0 0 14 0M12 18v3" fill="none" stroke="#111" strokeWidth="2" strokeLinecap="round" />
			</svg>
			{bars.map((b, i) => (
				<div key={i} style={{width: 7, height: 30 * b, borderRadius: 4, background: '#00c853'}} />
			))}
		</div>
	);
};

export const ChatBubble: React.FC<{x: number; y: number; text: string; age: number; scale?: number}> = ({x, y, text, age, scale = 1}) => {
	const pop = Math.min(1, age / 0.15);
	return (
		<div
			style={{
				position: 'absolute',
				left: x,
				top: y,
				transform: `translate(-50%, -100%) scale(${scale * (0.6 + 0.4 * pop)})`,
				transformOrigin: 'bottom center',
				opacity: pop,
			}}
		>
			<div
				style={{
					background: '#fff',
					color: '#222',
					fontFamily: UI_FONT,
					fontWeight: 600,
					fontSize: 32,
					padding: '10px 22px',
					borderRadius: 22,
					whiteSpace: 'nowrap',
					boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
				}}
			>
				{text}
			</div>
			<div style={{width: 0, height: 0, margin: '0 auto', borderLeft: '12px solid transparent', borderRight: '12px solid transparent', borderTop: '14px solid #fff'}} />
		</div>
	);
};

// ---------------------------------------------------------------- captions + touches
export const Captions: React.FC<{t: number; bottom?: number}> = ({t, bottom = 34}) => {
	const cue = VOICE_CUES.find((c) => t >= c.at && t <= c.at + voiceSec(c.id) + 0.15 && speakerOf(c.id) !== 'crowd');
	if (!cue) return null;
	const sp = speakerOf(cue.id);
	const k = Math.min(1, (t - cue.at) / 0.12);
	const text = voiceText(cue.id).replace('Req', 'REQ').replace('ninety nine', '99').replace('Ninety nine percent', '99%');
	return (
		<div style={{position: 'absolute', left: 0, right: 0, bottom, display: 'flex', justifyContent: 'center', opacity: k}}>
			<div
				style={{
					maxWidth: 1300,
					padding: '10px 26px',
					borderRadius: 14,
					background: 'rgba(0,0,0,0.62)',
					fontFamily: UI_FONT,
					fontSize: 42,
					fontWeight: sp === 'narr' ? 600 : 700,
					fontStyle: sp === 'narr' ? 'italic' : 'normal',
					color: '#fff',
					textAlign: 'center',
					lineHeight: 1.2,
				}}
			>
				{sp === 'req' ? <span style={{color: '#ffd23f'}}>REQ: </span> : null}
				{text}
			</div>
		</div>
	);
};

export const Touches: React.FC<{t: number}> = ({t}) => (
	<>
		{TAPS.filter(([at]) => t >= at - 0.12 && t <= at + 0.4).map(([at, x, y]) => {
			const k = t - at;
			const press = k < 0 ? 1 + k / 0.12 : 1;
			const o = k < 0 ? press : interpolate(k, [0, 0.4], [1, 0]);
			const s = k < 0 ? 0.8 : 1 + k * 1.2;
			return (
				<div
					key={at}
					style={{
						position: 'absolute',
						left: x - 40,
						top: y - 40,
						width: 80,
						height: 80,
						borderRadius: '50%',
						background: 'rgba(255,255,255,0.45)',
						border: '3px solid rgba(255,255,255,0.8)',
						opacity: o,
						transform: `scale(${s})`,
						boxShadow: '0 0 12px rgba(0,0,0,0.25)',
					}}
				/>
			);
		})}
	</>
);

export const DayCard: React.FC<{t: number; from: number; to: number; day: number}> = ({t, from, to, day}) => {
	if (t < from || t > to) return null;
	const o = interpolate(t, [from, from + 0.1, to - 0.1, to], [0, 1, 1, 0]);
	return (
		<div style={{position: 'absolute', left: 0, right: 0, top: 120, textAlign: 'center', opacity: o}}>
			<span
				style={{
					fontFamily: DOC_FONT,
					fontSize: 130,
					letterSpacing: 6,
					color: '#fff',
					textShadow: '0 6px 0 rgba(0,0,0,0.45), 0 0 30px rgba(0,0,0,0.5)',
				}}
			>
				DAY {day}
			</span>
		</div>
	);
};

export const GameButton: React.FC<{label: React.ReactNode; color?: string; x: number; y: number; pressed?: boolean; disabled?: boolean; w?: number}> = ({
	label,
	color = 'linear-gradient(#7dff8a,#25c244)',
	x,
	y,
	pressed,
	disabled,
	w = 420,
}) => (
	<div
		style={{
			position: 'absolute',
			left: x - w / 2,
			top: y - 52,
			width: w,
			height: 104,
			borderRadius: 30,
			background: disabled ? 'linear-gradient(#bdbdbd,#8a8a8a)' : color,
			border: '5px solid #1a1a2e',
			boxShadow: pressed ? 'inset 0 -2px 0 rgba(0,0,0,0.2)' : 'inset 0 -10px 0 rgba(0,0,0,0.2), 0 6px 0 rgba(0,0,0,0.35)',
			transform: `translateY(${pressed ? 5 : 0}px) scale(${pressed ? 0.96 : 1})`,
			display: 'flex',
			alignItems: 'center',
			justifyContent: 'center',
			gap: 12,
			...outlined,
			fontSize: 50,
		}}
	>
		{label}
	</div>
);

export const Toast: React.FC<{t: number; at: number; text: string; color?: string; dur?: number; y?: number; size?: number}> = ({
	t,
	at,
	text,
	color = '#ff4d4d',
	dur = 1.6,
	y = 330,
	size = 76,
}) => {
	const k = t - at;
	if (k < 0 || k > dur) return null;
	const pop = k < 0.15 ? 0.5 + (k / 0.15) * 0.6 : k < 0.25 ? 1.1 - ((k - 0.15) / 0.1) * 0.1 : 1;
	const o = interpolate(k, [0, 0.08, dur - 0.3, dur], [0, 1, 1, 0]);
	return (
		<div style={{position: 'absolute', left: 0, right: 0, top: y, textAlign: 'center', opacity: o, transform: `scale(${pop}) translateY(${-k * 12}px)`}}>
			<span style={{...outlined, WebkitTextStroke: '12px #1a1a2e', fontSize: size, color}}>{text}</span>
		</div>
	);
};

export const GameUI: React.FC<{t: number; talking: boolean; stick?: [number, number]; jump?: boolean; chatFrom?: number; petsim?: boolean}> = ({
	t,
	talking,
	stick = [0, 0],
	jump,
	chatFrom = 0,
	petsim = true,
}) => (
	<>
		{petsim ? (
			<>
				<Currency t={t} />
				<SideMenu />
			</>
		) : null}
		<ChatWindow t={t} from={chatFrom} />
		<TopBar talking={talking} t={t} />
		<Thumbstick x={stick[0]} y={stick[1]} />
		<JumpButton pressed={jump} />
	</>
);
