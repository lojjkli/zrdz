import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {ChatWindow, DOC_FONT, GAME_FONT, JumpButton, outlined, Thumbstick, TopBar, UI_FONT} from './HUD';
import {easeOut, range} from '../three/cam';

// ---------------------------------------------------------------- Murder Mystery 2 style HUD
const SideButton: React.FC<{label: string; icon: string; bg: string}> = ({label, icon, bg}) => (
	<div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2}}>
		<div
			style={{
				width: 84,
				height: 84,
				borderRadius: 16,
				background: bg,
				border: '4px solid #121212',
				boxShadow: 'inset 0 -8px 0 rgba(0,0,0,0.25), 0 4px 0 rgba(0,0,0,0.35)',
				display: 'flex',
				alignItems: 'center',
				justifyContent: 'center',
				fontSize: 44,
			}}
		>
			<span style={{fontFamily: '"Noto Color Emoji"'}}>{icon}</span>
		</div>
		<div style={{...outlined, WebkitTextStroke: '5px #121212', fontSize: 21}}>{label}</div>
	</div>
);

export const LobbyMenu: React.FC = () => (
	<div style={{position: 'absolute', right: 30, top: 200, display: 'flex', flexDirection: 'column', gap: 12}}>
		<SideButton label="Inventory" icon="🎒" bg="linear-gradient(#ffcf5a,#e89a0c)" />
		<SideButton label="Shop" icon="🔪" bg="linear-gradient(#ff7b7b,#d62828)" />
		<SideButton label="Emotes" icon="💃" bg="linear-gradient(#8fd3ff,#2a85d8)" />
	</div>
);

export const LevelBadge: React.FC = () => (
	<div style={{position: 'absolute', right: 28, top: 24, display: 'flex', alignItems: 'center', gap: 12}}>
		<div
			style={{
				height: 54,
				padding: '0 18px',
				borderRadius: 14,
				background: 'rgba(15,15,20,0.75)',
				border: '3px solid #121212',
				display: 'flex',
				alignItems: 'center',
				gap: 10,
				...outlined,
				WebkitTextStroke: '5px #121212',
				fontSize: 30,
			}}
		>
			<span style={{fontFamily: '"Noto Color Emoji"'}}>🪙</span> 12,480
		</div>
		<div style={{width: 64, height: 64, borderRadius: 32, background: 'linear-gradient(#b48cff,#6a3fd6)', border: '4px solid #121212', display: 'flex', alignItems: 'center', justifyContent: 'center', ...outlined, WebkitTextStroke: '5px #121212', fontSize: 28}}>
			47
		</div>
	</div>
);

export const LobbyTimer: React.FC<{t: number; endsAt: number}> = ({t, endsAt}) => {
	const left = Math.max(0, Math.ceil(endsAt - t));
	return (
		<div style={{position: 'absolute', left: 0, right: 0, top: 26, display: 'flex', justifyContent: 'center'}}>
			<div style={{...outlined, WebkitTextStroke: '7px #121212', fontSize: 40}}>
				{left > 0 ? `Next round in 0:${String(left).padStart(2, '0')}` : 'Starting...'}
			</div>
		</div>
	);
};

export const RoundTimer: React.FC<{t: number; start: number; map?: string}> = ({t, start, map = 'Mansion'}) => {
	const left = Math.max(0, 180 - Math.floor((t - start) * 1.6));
	return (
		<div style={{position: 'absolute', left: 0, right: 0, top: 22, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
			<div style={{...outlined, WebkitTextStroke: '8px #121212', fontSize: 52}}>
				{Math.floor(left / 60)}:{String(left % 60).padStart(2, '0')}
			</div>
			<div style={{...outlined, WebkitTextStroke: '5px #121212', fontSize: 26, color: '#d8d8d8', marginTop: -4}}>{map}</div>
		</div>
	);
};

export const CoinBag: React.FC<{coins: number}> = ({coins}) => (
	<div
		style={{
			position: 'absolute',
			right: 300,
			top: 950,
			height: 64,
			padding: '0 22px',
			borderRadius: 18,
			background: 'rgba(15,15,20,0.6)',
			border: '3px solid #121212',
			display: 'flex',
			alignItems: 'center',
			gap: 10,
			...outlined,
			WebkitTextStroke: '5px #121212',
			fontSize: 34,
		}}
	>
		<span style={{fontFamily: '"Noto Color Emoji"'}}>💰</span> {coins}/40
	</div>
);

export const RoleTag: React.FC = () => (
	<div style={{position: 'absolute', left: 30, bottom: 380, ...outlined, WebkitTextStroke: '6px #121212', fontSize: 34, color: '#5dff6b'}}>Innocent</div>
);

export const GameUI: React.FC<{
	t: number;
	talking: boolean;
	mode?: 'lobby' | 'round' | 'plain';
	stick?: [number, number];
	jump?: boolean;
	chatFrom?: number;
	roundStart?: number;
	lobbyEnds?: number;
	coins?: number;
	hideChat?: boolean;
}> = ({t, talking, mode = 'lobby', stick = [0, 0], jump, chatFrom = 0, roundStart = 30.6, lobbyEnds = 27.6, coins = 0, hideChat}) => (
	<>
		{mode === 'lobby' ? (
			<>
				<LevelBadge />
				<LobbyMenu />
				{lobbyEnds > 0 ? <LobbyTimer t={t} endsAt={lobbyEnds} /> : null}
			</>
		) : null}
		{mode === 'round' ? (
			<>
				<RoundTimer t={t} start={roundStart} />
				<CoinBag coins={coins} />
				<RoleTag />
			</>
		) : null}
		{hideChat ? null : <ChatWindow t={t} from={chatFrom} />}
		<TopBar talking={talking} t={t} />
		<Thumbstick x={stick[0]} y={stick[1]} />
		<JumpButton pressed={jump} />
	</>
);

// ---------------------------------------------------------------- role reveal ("You are... Innocent")
export const RoleReveal: React.FC<{t: number}> = ({t}) => {
	const you = range(t, 0.15, 0.5);
	const role = range(t, 1.0, 1.15);
	const out = range(t, 2.6, 3.0);
	const punch = t > 1.0 ? 1 + 0.25 * Math.max(0, 1 - (t - 1.0) / 0.25) : 0.6;
	return (
		<AbsoluteFill style={{background: '#000', opacity: 1 - out}}>
			<AbsoluteFill style={{background: 'radial-gradient(ellipse at center, rgba(40,160,60,0.35) 0%, rgba(0,0,0,0) 60%)', opacity: role}} />
			<div style={{position: 'absolute', left: 0, right: 0, top: 300, textAlign: 'center', ...outlined, WebkitTextStroke: '8px #000', fontSize: 70, opacity: you}}>
				You are...
			</div>
			<div
				style={{
					position: 'absolute',
					left: 0,
					right: 0,
					top: 400,
					textAlign: 'center',
					fontFamily: GAME_FONT,
					fontWeight: 700,
					fontSize: 190,
					color: '#3cff5a',
					WebkitTextStroke: '14px #04300c',
					paintOrder: 'stroke fill',
					opacity: role,
					transform: `scale(${punch})`,
					textShadow: '0 0 60px rgba(60,255,90,0.5)',
				}}
			>
				Innocent
			</div>
			<div style={{position: 'absolute', left: 0, right: 0, top: 650, textAlign: 'center', fontFamily: UI_FONT, fontWeight: 700, fontSize: 42, color: '#e6e6e6', opacity: role}}>
				Hide from the Murderer. Collect coins. Survive.
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- freeze-frame name card (doc style)
export const NameCard: React.FC<{t: number; at: number; name: string; sub: string; color: string; x?: number; y?: number; dur?: number}> = ({
	t,
	at,
	name,
	sub,
	color,
	x = 120,
	y = 640,
	dur = 1.2,
}) => {
	const k = t - at;
	if (k < 0 || k > dur) return null;
	const slide = easeOut(k / 0.2);
	const o = interpolate(k, [0, 0.08, dur - 0.12, dur], [0, 1, 1, 0]);
	return (
		<div style={{position: 'absolute', left: x, top: y, opacity: o, transform: `translateX(${(1 - slide) * -60}px)`}}>
			<div style={{fontFamily: DOC_FONT, fontSize: 150, color: '#fff', letterSpacing: 8, lineHeight: 1, textShadow: '0 6px 0 rgba(0,0,0,0.5)'}}>{name}</div>
			<div style={{height: 6, width: 380 * slide, background: color, margin: '6px 0 10px'}} />
			<div style={{fontFamily: UI_FONT, fontWeight: 700, fontSize: 36, color: '#fff', letterSpacing: 4, textShadow: '0 2px 6px rgba(0,0,0,0.8)'}}>{sub}</div>
		</div>
	);
};

// freeze-frame look: desaturated + bars, used while a name card is up
export const FreezeTint: React.FC<{on: boolean; color?: string}> = ({on, color = 'rgba(255,200,40,0.18)'}) =>
	on ? <AbsoluteFill style={{background: color, mixBlendMode: 'multiply', boxShadow: 'inset 0 0 220px rgba(0,0,0,0.75)'}} /> : null;

export const BigText: React.FC<{t: number; from: number; to: number; text: string; color?: string; stroke?: string; top?: number; size?: number}> = ({
	t,
	from,
	to,
	text,
	color = '#fff',
	stroke = '#121212',
	top = 150,
	size = 110,
}) => {
	if (t < from || t > to) return null;
	const k = t - from;
	const pop = k < 0.12 ? 0.6 + (k / 0.12) * 0.55 : k < 0.22 ? 1.15 - ((k - 0.12) / 0.1) * 0.15 : 1;
	const o = interpolate(t, [from, from + 0.06, to - 0.2, to], [0, 1, 1, 0]);
	return (
		<div style={{position: 'absolute', left: 0, right: 0, top, textAlign: 'center', opacity: o, transform: `scale(${pop})`}}>
			<span style={{fontFamily: GAME_FONT, fontWeight: 700, fontSize: size, color, WebkitTextStroke: `${size / 7}px ${stroke}`, paintOrder: 'stroke fill', whiteSpace: 'nowrap'}}>
				{text}
			</span>
		</div>
	);
};
