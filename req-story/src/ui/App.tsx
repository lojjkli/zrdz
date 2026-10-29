import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {GAME_FONT, RobloxLogo, RobuxIcon, UI_FONT} from './HUD';
import {easeOut} from '../three/cam';

const BG = '#111216';
const CARD = '#1d1f24';

const outlined = (stroke = 8): React.CSSProperties => ({
	fontFamily: GAME_FONT,
	fontWeight: 700,
	color: '#fff',
	WebkitTextStroke: `${stroke}px #1a1a2e`,
	paintOrder: 'stroke fill',
});

export const PS99Thumb: React.FC<{size: number; wide?: boolean}> = ({size, wide}) => {
	const w = wide ? size * (16 / 9) : size;
	const s = size / 300;
	return (
		<div
			style={{
				width: w,
				height: size,
				borderRadius: 18 * s,
				overflow: 'hidden',
				position: 'relative',
				background: 'radial-gradient(circle at 50% 30%, #fff6a8 0%, #ffcf4d 18%, #ff8bd1 45%, #7b5cff 80%, #4630c9 100%)',
			}}
		>
			{/* sun rays */}
			{new Array(12).fill(0).map((_, i) => (
				<div
					key={i}
					style={{
						position: 'absolute',
						left: w / 2 - 6 * s,
						top: -size * 0.6,
						width: 12 * s,
						height: size * 1.3,
						background: 'rgba(255,255,255,0.12)',
						transform: `rotate(${i * 30}deg)`,
						transformOrigin: `50% ${size * 0.9}px`,
					}}
				/>
			))}
			{/* cat pet */}
			<div
				style={{
					position: 'absolute',
					left: w / 2 - 70 * s,
					top: 40 * s,
					width: 140 * s,
					height: 120 * s,
					borderRadius: 38 * s,
					background: 'linear-gradient(#ffc56b,#ff9b2f)',
					border: `${5 * s}px solid #5a2d00`,
				}}
			>
				{[-1, 1].map((d) => (
					<div
						key={d}
						style={{
							position: 'absolute',
							top: -30 * s,
							left: 70 * s + d * 38 * s - 20 * s,
							width: 0,
							height: 0,
							borderLeft: `${20 * s}px solid transparent`,
							borderRight: `${20 * s}px solid transparent`,
							borderBottom: `${34 * s}px solid #ff9b2f`,
						}}
					/>
				))}
				{[-1, 1].map((d) => (
					<div
						key={d}
						style={{
							position: 'absolute',
							top: 40 * s,
							left: 70 * s + d * 30 * s - 13 * s,
							width: 26 * s,
							height: 32 * s,
							borderRadius: '50%',
							background: '#1a1a1a',
							boxShadow: `inset ${6 * s}px ${-6 * s}px 0 ${-2 * s}px #1a1a1a, inset ${-4 * s}px ${4 * s}px 0 0 #fff`,
						}}
					/>
				))}
				<div style={{position: 'absolute', top: 82 * s, left: 62 * s, width: 16 * s, height: 10 * s, borderRadius: '50%', background: '#ff5c8a'}} />
			</div>
			<div style={{position: 'absolute', left: 0, right: 0, bottom: 74 * s, textAlign: 'center', ...outlined(9 * s), fontSize: 36 * s, letterSpacing: 1}}>
				PET SIMULATOR
			</div>
			<div style={{position: 'absolute', left: 0, right: 0, bottom: -8 * s, textAlign: 'center', ...outlined(12 * s), fontSize: 96 * s, color: '#ffe14d'}}>
				99
			</div>
		</div>
	);
};

const OtherThumb: React.FC<{size: number; bg: string; icon: string; title: string}> = ({size, bg, icon, title}) => {
	const s = size / 300;
	return (
		<div style={{width: size, height: size, borderRadius: 18 * s, overflow: 'hidden', position: 'relative', background: bg}}>
			<div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 130 * s, fontFamily: '"Noto Color Emoji"'}}>
				{icon}
			</div>
			<div style={{position: 'absolute', left: 0, right: 0, bottom: 14 * s, textAlign: 'center', ...outlined(7 * s), fontSize: 34 * s}}>{title}</div>
		</div>
	);
};

const GAMES = [
	{title: 'Bean Obby', icon: '🫘', bg: 'linear-gradient(135deg,#7ee081,#1f9e57)', rating: 88, players: '23.1K'},
	{title: 'PS99', icon: '', bg: '', rating: 91, players: '412K'},
	{title: 'Lava Rush', icon: '🌋', bg: 'linear-gradient(135deg,#ffb347,#e0331f)', rating: 84, players: '41.7K'},
	{title: 'Pizza Shift', icon: '🍕', bg: 'linear-gradient(135deg,#fff176,#f9a825)', rating: 90, players: '18.2K'},
	{title: 'Tower Doom', icon: '🗼', bg: 'linear-gradient(135deg,#b388ff,#5e35b1)', rating: 79, players: '9.4K'},
	{title: 'Blox Racers', icon: '🏎️', bg: 'linear-gradient(135deg,#80d8ff,#1565c0)', rating: 86, players: '12.9K'},
];
const GAME_NAMES: Record<string, string> = {PS99: 'Pet Simulator 99'};

const Header: React.FC<{title: string}> = ({title}) => (
	<div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 110, display: 'flex', alignItems: 'center', padding: '0 56px', gap: 26}}>
		<RobloxLogo size={46} />
		<div style={{fontFamily: UI_FONT, fontWeight: 800, fontSize: 46, color: '#fff'}}>{title}</div>
		<div
			style={{
				marginLeft: 40,
				flex: 1,
				height: 60,
				borderRadius: 30,
				background: '#2a2c32',
				color: '#9a9ca3',
				fontFamily: UI_FONT,
				fontSize: 28,
				display: 'flex',
				alignItems: 'center',
				padding: '0 28px',
			}}
		>
			🔍&nbsp;&nbsp;Search
		</div>
		<div style={{display: 'flex', alignItems: 'center', gap: 10, color: '#fff', fontFamily: UI_FONT, fontWeight: 700, fontSize: 32}}>
			<RobuxIcon size={34} /> 1,699
		</div>
		<div style={{width: 56, height: 56, borderRadius: '50%', background: '#2a2c32', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 30}}>🔔</div>
	</div>
);

const TabBar: React.FC = () => {
	const tabs = [
		['🏠', 'Home'],
		['📈', 'Charts'],
		['🧍', 'Avatar'],
		['💬', 'Chat'],
		['☰', 'More'],
	];
	return (
		<div
			style={{
				position: 'absolute',
				left: 0,
				right: 0,
				bottom: 0,
				height: 104,
				background: '#16171b',
				borderTop: '1px solid #2a2c32',
				display: 'flex',
				justifyContent: 'space-around',
				alignItems: 'center',
			}}
		>
			{tabs.map(([i, l], k) => (
				<div key={l} style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2, opacity: k === 0 ? 1 : 0.6}}>
					<div style={{fontSize: 34, filter: k === 0 ? 'none' : 'grayscale(1)'}}>{i}</div>
					<div style={{fontFamily: UI_FONT, fontSize: 22, color: '#fff', fontWeight: 600}}>{l}</div>
				</div>
			))}
		</div>
	);
};

export const AppHome: React.FC<{t: number; press?: number}> = ({t, press = 0}) => {
	const scroll = interpolate(t, [0, 1.6], [0, 60], {extrapolateRight: 'clamp', easing: easeOut});
	return (
		<AbsoluteFill style={{background: BG}}>
			<Header title="Home" />
			<div style={{position: 'absolute', top: 140 - scroll * 0.3, left: 56, fontFamily: UI_FONT, color: '#fff', fontWeight: 800, fontSize: 38}}>
				Recommended For You &nbsp;<span style={{color: '#9a9ca3'}}>›</span>
			</div>
			<div style={{position: 'absolute', top: 210 - scroll * 0.3, left: 56 - scroll, display: 'flex', gap: 28}}>
				{GAMES.map((g, i) => (
					<div key={g.title} style={{width: 300, transform: i === 1 ? `scale(${1 - press * 0.05})` : undefined}}>
						{g.title === 'PS99' ? <PS99Thumb size={300} /> : <OtherThumb size={300} bg={g.bg} icon={g.icon} title={g.title} />}
						<div style={{fontFamily: UI_FONT, color: '#fff', fontWeight: 700, fontSize: 28, marginTop: 12, whiteSpace: 'nowrap'}}>{GAME_NAMES[g.title] ?? g.title}</div>
						<div style={{fontFamily: UI_FONT, color: '#9a9ca3', fontWeight: 600, fontSize: 24, marginTop: 4}}>
							👍 {g.rating}% &nbsp; 👥 {g.players}
						</div>
					</div>
				))}
			</div>
			<div style={{position: 'absolute', top: 690 - scroll * 0.3, left: 56, fontFamily: UI_FONT, color: '#fff', fontWeight: 800, fontSize: 38}}>
				Continue &nbsp;<span style={{color: '#9a9ca3'}}>›</span>
			</div>
			<div style={{position: 'absolute', top: 760 - scroll * 0.3, left: 56, display: 'flex', gap: 28}}>
				{GAMES.slice().reverse().map((g) => (
					<div key={g.title} style={{width: 300, height: 170, borderRadius: 18, background: g.bg || '#7b5cff', opacity: 0.9}} />
				))}
			</div>
			<TabBar />
		</AbsoluteFill>
	);
};

export const GamePage: React.FC<{t: number; press?: number}> = ({t, press = 0}) => {
	const slide = interpolate(t, [0, 0.3], [1, 0], {extrapolateRight: 'clamp', easing: easeOut});
	return (
		<AbsoluteFill style={{background: BG, transform: `translateX(${slide * 1920}px)`}}>
			<div style={{position: 'absolute', left: 56, top: 36, fontFamily: UI_FONT, fontSize: 48, color: '#fff'}}>‹</div>
			<div style={{position: 'absolute', left: 110, top: 120}}>
				<PS99Thumb size={500} wide />
			</div>
			<div style={{position: 'absolute', left: 110, top: 650, display: 'flex', gap: 10}}>
				{[0, 1, 2, 3].map((i) => (
					<div key={i} style={{width: 14, height: 14, borderRadius: 7, background: i === 0 ? '#fff' : '#555'}} />
				))}
			</div>
			<div style={{position: 'absolute', left: 1040, top: 120, right: 80, fontFamily: UI_FONT, color: '#fff'}}>
				<div style={{fontSize: 70, fontWeight: 800, lineHeight: 1.05}}>Pet Simulator 99</div>
				<div style={{fontSize: 30, color: '#9a9ca3', marginTop: 12, fontWeight: 600}}>
					By <span style={{color: '#fff', textDecoration: 'underline'}}>BIG Games</span> <span style={{color: '#3d8bff'}}>✔</span>
				</div>
				<div style={{display: 'flex', gap: 36, marginTop: 34, fontSize: 28, fontWeight: 700}}>
					<div>
						👍 91%<div style={{fontSize: 22, color: '#9a9ca3', fontWeight: 600}}>Rating</div>
					</div>
					<div>
						412,503<div style={{fontSize: 22, color: '#9a9ca3', fontWeight: 600}}>Active</div>
					</div>
					<div>
						9.8B+<div style={{fontSize: 22, color: '#9a9ca3', fontWeight: 600}}>Visits</div>
					</div>
					<div>
						All Ages<div style={{fontSize: 22, color: '#9a9ca3', fontWeight: 600}}>Maturity</div>
					</div>
				</div>
				<div
					style={{
						marginTop: 46,
						height: 120,
						borderRadius: 18,
						background: press > 0 ? '#2ab152' : '#33c35d',
						display: 'flex',
						alignItems: 'center',
						justifyContent: 'center',
						transform: `scale(${1 - press * 0.03})`,
					}}
				>
					<svg width="64" height="64" viewBox="0 0 24 24">
						<path d="M7 4l13 8-13 8z" fill="#fff" />
					</svg>
				</div>
				<div style={{marginTop: 40, fontSize: 28, color: '#c9cbd1', lineHeight: 1.45, fontWeight: 500}}>
					🎉 Hatch pets, collect diamonds and explore the world!
					<br />
					🎰 NEW: Lucky Spin machine in the Casino Zone
				</div>
			</div>
		</AbsoluteFill>
	);
};

export const Loading: React.FC<{t: number}> = ({t}) => {
	const o = interpolate(t, [0, 0.25], [0, 1], {extrapolateRight: 'clamp'});
	return (
		<AbsoluteFill style={{background: 'radial-gradient(circle at 50% 40%, #23252b, #0b0c0f)', opacity: o}}>
			<div style={{position: 'absolute', right: 60, top: 40, color: '#fff', fontFamily: UI_FONT, fontSize: 34, opacity: 0.8}}>✕</div>
			<div style={{position: 'absolute', left: '50%', top: 250, transform: 'translateX(-50%)', boxShadow: '0 20px 60px rgba(0,0,0,0.6)', borderRadius: 30}}>
				<PS99Thumb size={300} />
			</div>
			<div style={{position: 'absolute', left: 0, right: 0, top: 600, textAlign: 'center', fontFamily: UI_FONT, color: '#fff'}}>
				<div style={{fontSize: 56, fontWeight: 800}}>Pet Simulator 99</div>
				<div style={{fontSize: 30, color: '#9a9ca3', marginTop: 8, fontWeight: 600}}>
					By BIG Games <span style={{color: '#3d8bff'}}>✔</span>
				</div>
			</div>
			<div style={{position: 'absolute', left: '50%', top: 820, transform: `translateX(-50%) rotate(${t * 360}deg)`}}>
				<RobloxLogo size={70} />
			</div>
		</AbsoluteFill>
	);
};
