import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {easeOut, range} from '../three/cam';
import {rand} from '../three/textures';
import {GAME_FONT, outlined, RobuxIcon, UI_FONT} from './HUD';

// ---------------------------------------------------------------- robux counter (top right)
export const RobuxCounter: React.FC<{value: number; pulse?: number; gold?: boolean}> = ({value, pulse = 0, gold}) => (
	<div style={{position: 'absolute', right: 28, top: 24, transform: `scale(${1 + pulse * 0.18})`, transformOrigin: 'right top'}}>
		<div
			style={{
				height: 64,
				padding: '0 22px',
				borderRadius: 16,
				background: gold ? 'linear-gradient(#ffe27a,#d39a12)' : 'rgba(15,15,20,0.75)',
				border: '3px solid #121212',
				display: 'flex',
				alignItems: 'center',
				gap: 12,
				...outlined,
				WebkitTextStroke: '6px #121212',
				fontSize: 36,
				color: value === 0 ? '#ff6b6b' : '#fff',
			}}
		>
			<RobuxIcon size={32} />
			{Math.floor(value).toLocaleString('en-US')}
		</div>
	</div>
);

// ---------------------------------------------------------------- screen crack
export const CrackOverlay: React.FC<{t: number; at: number; dur?: number; x?: number; y?: number; seed?: number}> = ({t, at, dur = 2.8, x = 1180, y = 420, seed = 1}) => {
	const k = t - at;
	if (k < 0 || k > dur) return null;
	const grow = easeOut(k / 0.12);
	const o = interpolate(k, [0, 0.02, dur - 0.4, dur], [0, 1, 1, 0]);
	const rays = new Array(14).fill(0).map((_, i) => {
		const a = (i / 14) * Math.PI * 2 + rand(i + seed) * 0.4;
		let px = x;
		let py = y;
		let d = `M ${x} ${y}`;
		const len = 140 + rand(i * 3 + seed) * 520;
		for (let s = 1; s <= 5; s++) {
			const r = (len / 5) * grow;
			const j = (rand(i * 7 + s + seed) - 0.5) * 0.6;
			px += Math.cos(a + j) * r;
			py += Math.sin(a + j) * r;
			d += ` L ${px.toFixed(1)} ${py.toFixed(1)}`;
		}
		return d;
	});
	const rings = [60, 130, 230].map((r, i) => {
		let d = '';
		for (let s = 0; s <= 14; s++) {
			const a = (s / 14) * Math.PI * 2;
			const rr = r * grow * (0.8 + rand(s + i * 20 + seed) * 0.4);
			d += `${s === 0 ? 'M' : 'L'} ${(x + Math.cos(a) * rr).toFixed(1)} ${(y + Math.sin(a) * rr).toFixed(1)} `;
		}
		return d;
	});
	return (
		<AbsoluteFill style={{opacity: o}}>
			<svg width={1920} height={1080}>
				{[...rays, ...rings].map((d, i) => (
					<g key={i}>
						<path d={d} fill="none" stroke="rgba(0,0,0,0.45)" strokeWidth={5} />
						<path d={d} fill="none" stroke="rgba(255,255,255,0.9)" strokeWidth={2.2} />
					</g>
				))}
				<circle cx={x} cy={y} r={18 * grow} fill="rgba(255,255,255,0.7)" />
			</svg>
		</AbsoluteFill>
	);
};

export const Flash: React.FC<{t: number; at: number; dur?: number; color?: string}> = ({t, at, dur = 0.5, color = '#fff'}) => {
	const k = t - at;
	if (k < 0 || k > dur) return null;
	return <AbsoluteFill style={{background: color, opacity: 1 - k / dur}} />;
};

export const Fade: React.FC<{t: number; inAt: number; outFrom?: number; outTo?: number; inDur?: number}> = ({t, inAt, outFrom, outTo, inDur = 0.4}) => (
	<AbsoluteFill style={{background: '#000', opacity: Math.max(1 - range(t, inAt, inAt + inDur), outFrom !== undefined && outTo !== undefined ? range(t, outFrom, outTo) : 0)}} />
);

// ---------------------------------------------------------------- Roblox Studio (fake)
const S_BG = '#2e2e2e';
const S_PANEL = '#353535';
const S_LINE = '#222';

export type OutLine = {at: number; text: string; color?: string};

export const StudioUI: React.FC<{t: number; out: OutLine[]; explorer: string[]}> = ({t, out, explorer}) => {
	const lines = out.filter((l) => l.at <= t).slice(-6);
	const tabs = ['HOME', 'MODEL', 'AVATAR', 'TEST', 'VIEW', 'PLUGINS'];
	const tools = ['Select', 'Move', 'Scale', 'Rotate', 'Part', 'Material', 'Color', 'Group', 'Anchor', 'Play'];
	return (
		<AbsoluteFill style={{fontFamily: UI_FONT, color: '#ddd'}}>
			{/* title + tabs + ribbon */}
			<div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 150, background: S_BG, borderBottom: `2px solid ${S_LINE}`}}>
				<div style={{height: 38, display: 'flex', alignItems: 'center', padding: '0 18px', gap: 24, fontSize: 20, background: '#252525'}}>
					<span style={{fontWeight: 800, color: '#fff'}}>Roblox Studio</span>
					<span>File</span>
					<span style={{marginLeft: 'auto', color: '#aaa'}}>kli's Obby (1).rbxl — not saved</span>
				</div>
				<div style={{height: 34, display: 'flex', alignItems: 'center', gap: 28, padding: '0 18px', fontSize: 18, fontWeight: 700}}>
					{tabs.map((x, i) => (
						<span key={x} style={{color: i === 0 ? '#fff' : '#9a9a9a', borderBottom: i === 0 ? '3px solid #00a2ff' : 'none', paddingBottom: 4}}>
							{x}
						</span>
					))}
				</div>
				<div style={{display: 'flex', gap: 10, padding: '6px 18px'}}>
					{tools.map((x, i) => (
						<div key={x} style={{width: 74, height: 62, borderRadius: 6, background: i === 4 ? '#3f5c78' : 'transparent', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 4, fontSize: 15}}>
							<div style={{width: 30, height: 26, borderRadius: 4, background: ['#5aa9ff', '#7ad37a', '#ffb347', '#ff7a7a', '#cfcfcf', '#b98cff', '#ffd84d', '#8fd3ff', '#cccccc', '#4fdc6a'][i]}} />
							{x}
						</div>
					))}
				</div>
			</div>
			{/* explorer + properties */}
			<div style={{position: 'absolute', right: 0, top: 150, bottom: 0, width: 360, background: S_PANEL, borderLeft: `2px solid ${S_LINE}`}}>
				<div style={{padding: '10px 14px', fontSize: 19, fontWeight: 800, background: S_BG}}>Explorer</div>
				<div style={{padding: '8px 14px', fontSize: 19, lineHeight: '30px'}}>
					{['Workspace', ...explorer.map((e) => '   ' + e), 'Players', 'Lighting', 'ReplicatedStorage', 'ServerScriptService', 'StarterGui'].slice(0, 16).map((e, i) => (
						<div key={i} style={{whiteSpace: 'pre', color: e.includes('Baseplate') && t > 83.6 ? '#ff6b6b' : '#ddd'}}>
							{e.startsWith('   ') ? '   ▸ ' + e.trim() : '▾ ' + e}
						</div>
					))}
				</div>
				<div style={{position: 'absolute', left: 0, right: 0, top: 620, padding: '10px 14px', fontSize: 19, fontWeight: 800, background: S_BG}}>Properties</div>
				<div style={{position: 'absolute', left: 14, right: 14, top: 670, fontSize: 18, lineHeight: '30px', color: '#bbb'}}>
					{[
						['Anchored', '☐'],
						['CanCollide', '☑'],
						['Color', 'Really red'],
						['Material', 'Plastic'],
						['Size', '4, 1, 2'],
					].map(([a, b]) => (
						<div key={a} style={{display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #2a2a2a'}}>
							<span>{a}</span>
							<span style={{color: a === 'Anchored' ? '#ff6b6b' : '#ddd'}}>{b}</span>
						</div>
					))}
				</div>
			</div>
			{/* output */}
			<div style={{position: 'absolute', left: 0, right: 360, bottom: 0, height: 230, background: S_PANEL, borderTop: `2px solid ${S_LINE}`}}>
				<div style={{padding: '8px 14px', fontSize: 19, fontWeight: 800, background: S_BG}}>Output</div>
				<div style={{padding: '6px 16px', fontFamily: '"Source Sans 3", monospace', fontSize: 21, lineHeight: '29px'}}>
					{lines.map((l, i) => (
						<div key={l.at + l.text} style={{color: l.color ?? '#ff5b5b', opacity: Math.min(1, (t - l.at) / 0.1), whiteSpace: 'nowrap'}}>
							{`${String(14 + Math.floor(l.at / 60)).padStart(2, '0')}:${String(Math.floor(l.at) % 60).padStart(2, '0')}:${String(Math.floor((l.at % 1) * 1000)).padStart(3, '0')}`}  {l.text}
						</div>
					))}
				</div>
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- the 3D app (Blender-like, no logos)
const B_BG = '#303030';
const B_HEAD = '#3d3d3d';

export const BlenderUI: React.FC<{t: number; outliner: string[]; title?: string}> = ({t, outliner, title = 'untitled.blend'}) => (
	<AbsoluteFill style={{fontFamily: UI_FONT, color: '#d6d6d6'}}>
		<div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 44, background: '#232323', display: 'flex', alignItems: 'center', gap: 26, padding: '0 16px', fontSize: 19}}>
			<div style={{width: 26, height: 26, borderRadius: 13, background: 'radial-gradient(circle,#2f6fd6 40%,#ff8a1f 42%)'}} />
			{['File', 'Edit', 'Render', 'Window', 'Help'].map((x) => (
				<span key={x}>{x}</span>
			))}
			{['Layout', 'Modeling', 'Sculpting', 'UV Editing', 'Texture Paint', 'Shading', 'Animation'].map((x, i) => (
				<span key={x} style={{padding: '4px 12px', borderRadius: 6, background: i === 0 ? '#4a4a4a' : 'transparent', color: i === 0 ? '#fff' : '#aaa'}}>
					{x}
				</span>
			))}
			<span style={{marginLeft: 'auto', color: '#999'}}>{title}</span>
		</div>
		<div style={{position: 'absolute', left: 0, right: 400, top: 44, height: 42, background: B_HEAD, display: 'flex', alignItems: 'center', gap: 22, padding: '0 16px', fontSize: 18}}>
			<span style={{padding: '3px 12px', borderRadius: 6, background: '#2b2b2b'}}>Object Mode ▾</span>
			{['View', 'Select', 'Add', 'Object'].map((x) => (
				<span key={x}>{x}</span>
			))}
			<span style={{marginLeft: 'auto', color: '#aaa'}}>Global ▾</span>
		</div>
		{/* left toolbar */}
		<div style={{position: 'absolute', left: 10, top: 110, width: 48, display: 'flex', flexDirection: 'column', gap: 6}}>
			{new Array(9).fill(0).map((_, i) => (
				<div key={i} style={{width: 48, height: 46, borderRadius: 8, background: i === 0 ? '#4772b3' : '#2b2b2b', border: '1px solid #1f1f1f'}} />
			))}
		</div>
		{/* nav gizmo */}
		<svg width={140} height={140} style={{position: 'absolute', right: 430, top: 110}}>
			<circle cx={70} cy={70} r={64} fill="rgba(255,255,255,0.05)" />
			<line x1={70} y1={70} x2={122} y2={92} stroke="#e0485d" strokeWidth={4} />
			<line x1={70} y1={70} x2={30} y2={100} stroke="#8bc34a" strokeWidth={4} />
			<line x1={70} y1={70} x2={70} y2={14} stroke="#4f8fe0" strokeWidth={4} />
			<circle cx={122} cy={92} r={13} fill="#e0485d" />
			<circle cx={30} cy={100} r={13} fill="#8bc34a" />
			<circle cx={70} cy={14} r={13} fill="#4f8fe0" />
			{[
				['X', 122, 97],
				['Y', 30, 105],
				['Z', 70, 19],
			].map(([l, x, y]) => (
				<text key={l as string} x={x as number} y={y as number} fontSize={16} fontWeight={800} textAnchor="middle" fill="#111">
					{l}
				</text>
			))}
		</svg>
		{/* right: outliner + properties */}
		<div style={{position: 'absolute', right: 0, top: 44, bottom: 0, width: 400, background: B_BG, borderLeft: '3px solid #1d1d1d'}}>
			<div style={{padding: '10px 14px', fontSize: 18, background: B_HEAD}}>Scene Collection</div>
			<div style={{padding: '8px 14px', fontSize: 19, lineHeight: '32px'}}>
				<div>▾ Collection</div>
				{outliner.map((o) => (
					<div key={o} style={{paddingLeft: 26, color: o === outliner[outliner.length - 1] ? '#ffa21a' : '#d6d6d6'}}>
						▸ {o}
					</div>
				))}
			</div>
			<div style={{position: 'absolute', left: 0, right: 0, top: 360, bottom: 0, background: '#2a2a2a', borderTop: '3px solid #1d1d1d'}}>
				<div style={{display: 'flex', flexDirection: 'column', gap: 12, padding: 16}}>
					{['Location', 'Rotation', 'Scale'].map((x) => (
						<div key={x}>
							<div style={{fontSize: 17, color: '#aaa', marginBottom: 6}}>{x}</div>
							{['X', 'Y', 'Z'].map((a) => (
								<div key={a} style={{height: 30, borderRadius: 6, background: '#545454', marginBottom: 4, fontSize: 16, lineHeight: '30px', padding: '0 10px', display: 'flex', justifyContent: 'space-between'}}>
									<span>{a}</span>
									<span>{x === 'Scale' ? '1.000' : '0 m'}</span>
								</div>
							))}
						</div>
					))}
				</div>
			</div>
		</div>
		{/* timeline */}
		<div style={{position: 'absolute', left: 0, right: 400, bottom: 0, height: 110, background: B_BG, borderTop: '3px solid #1d1d1d'}}>
			<div style={{display: 'flex', gap: 22, padding: '8px 16px', fontSize: 17, color: '#aaa'}}>
				<span>Playback ▾</span>
				<span>Keying ▾</span>
				<span>View</span>
				<span>Marker</span>
			</div>
			<div style={{position: 'absolute', left: 16, right: 16, bottom: 18, height: 34, display: 'flex', justifyContent: 'space-between', fontSize: 16, color: '#888'}}>
				{new Array(13).fill(0).map((_, i) => (
					<span key={i}>{i * 20}</span>
				))}
			</div>
			<div style={{position: 'absolute', left: 16 + ((t * 24) % 240) * 5.6, bottom: 14, width: 4, height: 60, background: '#4772b3'}} />
		</div>
	</AbsoluteFill>
);

// ---------------------------------------------------------------- kli's game page
export const ObbyPage: React.FC<{t: number; dislikeAt: number}> = ({t, dislikeAt}) => {
	const slide = interpolate(t, [0, 0.3], [1, 0], {extrapolateRight: 'clamp', easing: easeOut});
	const d = t >= dislikeAt;
	const pop = d ? 1 + 0.4 * Math.max(0, 1 - (t - dislikeAt) / 0.25) : 1;
	return (
		<AbsoluteFill style={{background: '#111216', transform: `translateX(${slide * 1920}px)`, fontFamily: UI_FONT, color: '#fff'}}>
			<div style={{position: 'absolute', left: 110, top: 120, width: 860, height: 484, borderRadius: 22, overflow: 'hidden', background: 'linear-gradient(#7ec8ff,#c9ecff)'}}>
				{/* ugly thumbnail: a few crooked bricks over lava */}
				<div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 150, background: 'linear-gradient(#ff7a00,#c42a00)'}} />
				{[
					[90, 270, -14, '#e53935'],
					[330, 230, 22, '#1e88e5'],
					[560, 300, -35, '#43a047'],
				].map(([x, y, r, c], i) => (
					<div key={i} style={{position: 'absolute', left: x as number, top: y as number, width: 170, height: 46, background: c as string, transform: `rotate(${r}deg)`, border: '4px solid rgba(0,0,0,0.3)'}} />
				))}
				<div style={{position: 'absolute', left: 30, top: 24, fontFamily: GAME_FONT, fontWeight: 700, fontSize: 86, color: '#ffeb3b', WebkitTextStroke: '10px #222', paintOrder: 'stroke fill', transform: 'rotate(-4deg)'}}>
					kli's obby!!!
				</div>
				<div style={{position: 'absolute', right: 30, top: 140, fontFamily: '"Noto Color Emoji"', fontSize: 90}}>🔥</div>
			</div>
			<div style={{position: 'absolute', left: 1040, top: 120, right: 80}}>
				<div style={{fontSize: 70, fontWeight: 800, lineHeight: 1.05}}>kli's Obby (1)</div>
				<div style={{fontSize: 30, color: '#9a9ca3', marginTop: 12, fontWeight: 600}}>
					By <span style={{color: '#fff', textDecoration: 'underline'}}>lojjkli</span>
				</div>
				<div style={{display: 'flex', gap: 40, marginTop: 34, fontSize: 30, fontWeight: 700}}>
					<div>
						👍 {d ? '0%' : '--'}
						<div style={{fontSize: 22, color: '#9a9ca3', fontWeight: 600}}>Rating</div>
					</div>
					<div style={{color: '#7cff8a'}}>
						1<div style={{fontSize: 22, color: '#9a9ca3', fontWeight: 600}}>Active</div>
					</div>
					<div>
						1<div style={{fontSize: 22, color: '#9a9ca3', fontWeight: 600}}>Visits</div>
					</div>
					<div style={{color: d ? '#ff5b5b' : '#fff', transform: `scale(${pop})`, transformOrigin: 'left center'}}>
						👎 {d ? 1 : 0}
						<div style={{fontSize: 22, color: '#9a9ca3', fontWeight: 600}}>Dislikes</div>
					</div>
				</div>
				<div style={{marginTop: 46, height: 120, borderRadius: 18, background: '#33c35d', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
					<svg width="64" height="64" viewBox="0 0 24 24">
						<path d="M7 4l13 8-13 8z" fill="#fff" />
					</svg>
				</div>
				<div style={{marginTop: 34, fontSize: 28, color: '#c9cbd1', lineHeight: 1.45, fontWeight: 500}}>
					my first game!!! pls like 🥺
					<br />
					<span style={{color: '#888'}}>(the lava is supposed to be there)</span>
				</div>
				{t > dislikeAt + 0.6 ? (
					<div style={{marginTop: 26, padding: '16px 20px', borderRadius: 14, background: '#1d1f25', fontSize: 26, opacity: Math.min(1, (t - dislikeAt - 0.6) / 0.2)}}>
						<b style={{color: '#ffd166'}}>Toast_YT</b>: worst game ever 💀 i fell through the floor
					</div>
				) : null}
			</div>
		</AbsoluteFill>
	);
};

// ---------------------------------------------------------------- title pop words
export const PopWords: React.FC<{t: number; words: {at: number; text: string; color?: string; x: number; y: number; rot?: number}[]; until: number}> = ({t, words, until}) => (
	<>
		{words.map((w) => {
			if (t < w.at || t > until) return null;
			const k = t - w.at;
			const s = k < 0.12 ? 0.4 + (k / 0.12) * 0.8 : k < 0.22 ? 1.2 - ((k - 0.12) / 0.1) * 0.2 : 1;
			return (
				<div
					key={w.text}
					style={{
						position: 'absolute',
						left: w.x,
						top: w.y,
						transform: `translate(-50%,-50%) scale(${s}) rotate(${w.rot ?? 0}deg)`,
						fontFamily: GAME_FONT,
						fontWeight: 700,
						fontSize: 96,
						color: w.color ?? '#fff',
						WebkitTextStroke: '14px #121212',
						paintOrder: 'stroke fill',
						whiteSpace: 'nowrap',
						opacity: interpolate(t, [until - 0.2, until], [1, 0], {extrapolateLeft: 'clamp'}),
					}}
				>
					{w.text}
				</div>
			);
		})}
	</>
);
