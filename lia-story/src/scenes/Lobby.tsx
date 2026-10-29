import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {ADE_LOOK, Avatar, LIA_LOOK, MIKEY_LOOK, npcLook, REQ_LOOK} from '../three/Avatar';
import {Cam, clamp01, ease, lerp, lerp3, range, V3} from '../three/cam';
import {Clouds, Stage} from '../three/World';
import {Lobby, LOBBY_DAY} from '../three/MM2World';
import {bubbleOf, FPS, talking} from '../timeline';
import {Billboards} from '../ui/Billboards';
import {FreezeTint, GameUI, NameCard} from '../ui/MM2';
import {face, Shot, shotAt} from './shots';

const Y = 0.4; // plaza top
const WALK0 = 15.0;
const WALK1 = 17.8;
const LIA_FROM: V3 = [0, Y, 17];
const LIA_TO: V3 = [0, Y, 6.5];
export const REQ_AT: V3 = [-4.2, Y, -0.5];
export const MIKEY_AT: V3 = [0.2, Y, -2.2];
export const ADE_AT: V3 = [4.4, Y, -0.3];

const liaPos = (t: number): V3 => lerp3(LIA_FROM, LIA_TO, clamp01((t - WALK0) / (WALK1 - WALK0)));

// freeze-frame name cards
const CARDS = [
	{at: 18.0, to: 19.2, who: REQ_AT, name: 'REQ', sub: 'RECOVERING GAMBLER', color: '#ffd23f'},
	{at: 19.2, to: 20.4, who: MIKEY_AT, name: 'MIKEY', sub: 'SAYS "BRO" 400 TIMES A DAY', color: '#7ad3ff'},
	{at: 20.4, to: 21.7, who: ADE_AT, name: 'ADE', sub: 'ACTUALLY GOOD AT MM2', color: '#9cff8a'},
];

const STRANGERS: {p: V3; i: number; rot: number; walk?: number}[] = [
	{p: [-16, Y, -12], i: 3, rot: 0.4},
	{p: [15, Y, -13], i: 8, rot: -0.6},
	{p: [-20, Y, 8], i: 5, rot: 1.2, walk: 1},
	{p: [19, Y, 3], i: 10, rot: -1.4},
];

const SHOTS: Shot[] = [
	// spawn: behind Lia, following
	{
		from: 14,
		to: 18,
		cam: (t) => {
			const p = liaPos(t);
			return {pos: [p[0] + 3.2, 8.2, p[2] + 13.5], target: [p[0] - 0.5, 4.2, p[2] - 8], fov: 52};
		},
	},
	// freeze cards: one close shot per friend
	...CARDS.map((c) => ({
		from: c.at,
		to: c.to,
		cam: (t: number, k: number) => ({pos: [c.who[0] + 3.5 - k * 0.4, 5.6, c.who[2] + 7.5 - k * 0.6] as V3, target: [c.who[0] - 0.4, 4.6, c.who[2]] as V3, fov: 40}),
	})),
	// group: over Lia's shoulder at the friends
	{from: 21.7, to: 25.5, cam: (t, k) => ({pos: lerp3([3.0, 6.2, 13.5], [2.4, 5.9, 12.2], ease(k)), target: [-0.6, 4.2, 0], fov: 46})},
	// REQ: "wait, I'm bringing someone"
	{from: 25.5, to: 27.6, cam: (t, k) => ({pos: lerp3([-1.2, 5.4, 4.2], [-1.8, 5.3, 3.4], k), target: [REQ_AT[0], 4.7, REQ_AT[2]], fov: 42})},
];

export const LobbyScene: React.FC<{t0: number}> = ({t0}) => {
	const frame = useCurrentFrame();
	const t = t0 + frame / FPS;
	const card = CARDS.find((c) => t >= c.at && t < c.to);
	// while a name card is up the world is frozen at the moment the card appeared
	const tv = card ? card.at : t;
	const {cam} = shotAt(SHOTS, t);
	const lia = liaPos(tv);
	const walking = tv > WALK0 && tv < WALK1;
	const walkAmt = walking ? Math.min(1, (tv - WALK0) * 4, (WALK1 - tv) * 4) : 0;
	const liaTalk = talking('lia', tv);
	const hop = tv > 23.0 && tv < 23.6 ? Math.sin(((tv - 23.0) / 0.6) * Math.PI) * 1.6 : 0;
	const friends = [
		{look: REQ_LOOK, p: REQ_AT, name: 'REQ', wave: 0, talk: talking('req', tv)},
		{look: MIKEY_LOOK, p: MIKEY_AT, name: 'Mikey', wave: tv > 15.9 && tv < 17.6 ? 1 : 0, talk: false},
		{look: ADE_LOOK, p: ADE_AT, name: 'Ade', wave: tv > 16.8 && tv < 18.0 ? 1 : 0, talk: false},
	];
	const lookAtLia = (p: V3) => face(p, lia);
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...LOBBY_DAY, shadowCenter: [0, 0, 5], shadowSize: 34}}>
				<Lobby t={tv} />
				<Clouds t={tv} />
				<Avatar
					look={{...LIA_LOOK}}
					position={lia}
					rotationY={walking || tv < WALK0 ? Math.PI : Math.PI + lerp(0, -0.25, range(tv, 25.5, 26.2))}
					pose={{walk: (tv - WALK0) * 9, walkAmt, time: tv, jump: hop, armsUp: hop > 0 ? 0.6 : 0, wave: tv > 17.6 && tv < 18.0 ? 1 : 0}}
				/>
				{friends.map((f, i) => (
					<Avatar
						key={f.name}
						look={f.look}
						position={f.p}
						rotationY={i === 0 && tv > 25.4 ? lerp(lookAtLia(f.p), lookAtLia(f.p) + 0.9, range(tv, 25.4, 25.9)) : lookAtLia(f.p)}
						pose={{time: tv + i * 1.3, wave: f.wave, jump: tv > 24.6 && tv < 25.2 && i > 0 ? Math.sin(((tv - 24.6) / 0.6) * Math.PI) : 0}}
					/>
				))}
				{STRANGERS.map((s) => (
					<Avatar key={s.i} look={npcLook(s.i)} position={s.walk ? [s.p[0] + Math.sin(tv * 0.3) * 4, Y, s.p[2] + Math.cos(tv * 0.3) * 4] : s.p} rotationY={s.walk ? -tv * 0.3 : s.rot} pose={{time: tv + s.i, walk: tv * 9, walkAmt: s.walk ?? 0}} />
				))}
			</Stage>
			<Billboards
				cam={cam}
				t={tv}
				items={[
					{p: lia, talking: liaTalk},
					...friends.map((f) => ({p: f.p, name: f.name, talking: f.talk, bubble: bubbleOf(f.name, tv)})),
					...STRANGERS.map((s) => ({p: s.p, name: ['xXslasherXx', 'Toast_YT', 'bacon_hair2012', 'Lilyy_bloom'][STRANGERS.indexOf(s)]})),
				]}
			/>
			<GameUI t={tv} talking={liaTalk} mode="lobby" stick={walking ? [0, -walkAmt] : [0, 0]} jump={hop > 0} />
			<FreezeTint on={!!card} />
			{CARDS.map((c) => (
				<NameCard key={c.name} t={t} at={c.at} dur={c.to - c.at} name={c.name} sub={c.sub} color={c.color} />
			))}
			{/* spawn fade in, fade out into the role reveal */}
			<AbsoluteFill style={{background: '#000', opacity: Math.max(1 - clamp01((t - t0) / 0.4), range(t, 27.25, 27.6))}} />
		</AbsoluteFill>
	);
};
