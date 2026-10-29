import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Avatar, MYNINN_LOOK, NOOB_KLI, npcLook} from '../three/Avatar';
import {Cam, clamp01, ease, lerp, lerp3, range, V3} from '../three/cam';
import {Rain, Sparkles, Spotlight} from '../three/Props';
import {Clouds, Env, lerpEnv, Stage} from '../three/World';
import {Lobby, LOBBY_DAY, LOBBY_NIGHT} from '../three/MM2World';
import {Alley, Bread, CardboardBox, Pigeon} from '../three/KliProps';
import {rand, signTexture} from '../three/textures';
import {bubbleOf, FPS, HATERS, LEAVES, talking} from '../timeline';
import {Billboards} from '../ui/Billboards';
import {DOC_FONT, UI_FONT} from '../ui/HUD';
import {DisconnectDialog} from '../ui/Dialogs';
import {BigText, FreezeTint, GameUI, NameCard} from '../ui/MM2';
import {CrackOverlay, Fade, Flash, PopWords, RobuxCounter} from '../ui/KliUI';
import {Grain, Letterbox, Vignette} from './Doc';
import {face, Shot, shotAt, withShake} from './shots';

export const VOID: Env = {
	skyTop: '#04020a',
	skyHorizon: '#0c0a1c',
	sunDir: [0.3, 1, 0.4],
	sunColor: '#b8a8ff',
	sunIntensity: 0.15,
	hemiSky: '#334',
	hemiGround: '#000',
	hemiIntensity: 0.25,
	fog: ['#05040c', 20, 70],
	sunGlow: 0,
};

// ================================================================ cold open
export const KliColdOpen: React.FC = () => {
	const t = useCurrentFrame() / FPS;
	const k = ease(range(t, 0, 7));
	const cam: Cam = {pos: lerp3([0.2, 5.0, 6.6], [4.5, 4.4, 14], k), target: lerp3([-1.3, 4.6, 0], [-3.4, 3.4, 0], k), fov: 40};
	const dust = new Array(40).fill(0).map((_, i) => [(rand(i) - 0.5) * 14, (rand(i + 1) * 10 + t * 0.3 * (0.5 + rand(i + 2))) % 10, (rand(i + 3) - 0.5) * 10] as V3);
	const title = range(t, 0.9, 1.5);
	const sub = range(t, 3.0, 3.6);
	const out = range(t, 6.5, 7);
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<Stage cam={cam} env={VOID}>
				<mesh position={[0, -0.25, 0]} receiveShadow>
					<cylinderGeometry args={[4, 4.3, 0.5, 48]} />
					<meshStandardMaterial color="#1f1f2c" roughness={0.3} metalness={0.4} />
				</mesh>
				<Spotlight position={[0, 22, 3]} target={[0, 0, 0]} intensity={1600} color="#e6e6ff" />
				<pointLight position={[-6, 4, -6]} color="#7b5cff" intensity={70} distance={30} />
				<pointLight position={[2, 4.5, 7]} color="#e0dcff" intensity={22} distance={16} />
				<Avatar look={NOOB_KLI} position={[0, 0, 0]} rotationY={0.25} pose={{time: t, headYaw: -0.5 + ease(range(t, 2.0, 3.2)) * 0.6}} />
				<Sparkles points={dust} t={t} color="#8a8aa8" size={0.05} />
			</Stage>
			<Vignette />
			<div style={{position: 'absolute', left: 150, top: 330, opacity: title, transform: `translateX(${(1 - title) * -40}px)`}}>
				<div style={{fontFamily: DOC_FONT, fontSize: 300, color: '#fff', letterSpacing: 40, lineHeight: 1}}>KLI</div>
				<div style={{height: 4, width: 520 * title, background: '#8f7bff', marginTop: 10}} />
				<div style={{fontFamily: UI_FONT, fontSize: 40, color: '#d8d8d8', marginTop: 24, letterSpacing: 10, opacity: sub, fontWeight: 600}}>
					FROM SQUEAK TO LEGEND
				</div>
			</div>
			<Grain t={t} />
			<Letterbox h={110 * (1 - out)} />
			<AbsoluteFill style={{background: '#000', opacity: Math.max(1 - t / 0.7, out)}} />
		</AbsoluteFill>
	);
};

// ================================================================ the squeak
const Y = 0.4;
const K_FROM: V3 = [0, Y, 17];
const K_TO: V3 = [0, Y, 6.5];
const kliPos = (t: number): V3 => lerp3(K_FROM, K_TO, range(t, 7.2, 9.4));
const NPCS: {p: V3; i: number}[] = [
	{p: [-4.2, Y, -0.5], i: 3},
	{p: [0.2, Y, -2.2], i: 8},
	{p: [4.4, Y, -0.3], i: 10},
	{p: [-8.2, Y, 2.6], i: 5},
];
const LEAVE_START = 16.6;
const npcPos = (n: (typeof NPCS)[number], t: number): V3 => {
	const w = Math.max(0, t - LEAVE_START);
	return [n.p[0] + Math.sign(n.p[0] + 0.01) * w * 0.8, Y, n.p[2] - w * 3.2];
};

const SQ_SHOTS: Shot[] = [
	{from: 7, to: 9.6, cam: (t) => {
		const p = kliPos(t);
		return {pos: [p[0] + 3.2, 8.2, p[2] + 13.5], target: [p[0] - 0.5, 4.2, p[2] - 8], fov: 52};
	}},
	{from: 9.6, to: 11.5, cam: (t, k) => ({pos: lerp3([1.6, 5.0, 0.6], [1.3, 4.9, 1.4], k), target: [0, 4.6, K_TO[2]], fov: 44})},
	{from: 11.5, to: 13.6, cam: (t, k) => ({pos: lerp3([2.4, 6.2, 13.0], [2.0, 6.0, 12.2], k), target: [-0.6, 4.4, 0], fov: 46})},
	{from: 13.6, to: 16.6, cam: (t, k) => ({pos: lerp3([0.7, 4.9, K_TO[2] - 5.5], [0.3, 4.8, K_TO[2] - 3.6], ease(k)), target: [0, 4.7, K_TO[2]], fov: 42})},
	{from: 16.6, to: 20.2, cam: (t, k) => ({pos: lerp3([15, 7, 6], [14, 7.5, 8], k), target: [0, 3.5, 2], fov: 50})},
	{from: 20.2, to: 31, cam: (t, k) => ({pos: lerp3([5, 9, 18], [9, 28, 24], ease(range(t, 20.2, 25))), target: [0, 2.5, K_TO[2]], fov: 48})},
];

export const SqueakScene: React.FC<{t0: number}> = ({t0}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const base = shotAt(SQ_SHOTS, t).cam;
	const cam = withShake(base, t, t > 11.6 && t < 12.4 ? 0.12 * (1 - (t - 11.6) / 0.8) : 0);
	const kp = kliPos(t);
	const walking = t > 7.2 && t < 9.4;
	const walkAmt = walking ? Math.min(1, (t - 7.2) * 4, (9.4 - t) * 4) : 0;
	const kTalk = talking('kli', t);
	const kFace = t < 11.5 ? 'smile' : t < 20 ? 'worried' : 'sad';
	const npcs = NPCS.map((n, j) => ({...n, j, gone: t >= LEAVES[j], pos: npcPos(n, t)}));
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...LOBBY_DAY, shadowCenter: [0, 0, 5], shadowSize: 34}}>
				<Lobby t={t} />
				<Clouds t={t} />
				<Avatar
					look={{...NOOB_KLI, face: kFace}}
					position={kp}
					rotationY={Math.PI}
					pose={{walk: (t - 7.2) * 9, walkAmt, time: t, wave: t > 9.8 && t < 11.4 ? 1 : 0, point: t > 16.8 && t < 18.4 ? 1 : 0, headPitch: t > 20 ? 0.3 : 0}}
				/>
				{npcs.map((n) =>
					n.gone ? null : (
						<Avatar
							key={n.i}
							look={{...npcLook(n.i), face: t < 11.5 ? 'smile' : t < 16.6 ? 'shock' : 'angry'}}
							position={n.pos}
							rotationY={t < LEAVE_START ? face(n.p, kp) : lerp(face(n.p, kp), face(n.p, kp) + Math.PI, range(t, LEAVE_START, LEAVE_START + 0.4))}
							pose={{time: t + n.j, walk: t * 9, walkAmt: t > LEAVE_START + 0.3 ? 1 : 0, cover: t > 11.6 && t < 14.0 ? 1 : 0}}
						/>
					),
				)}
			</Stage>
			<Billboards
				cam={cam}
				t={t}
				items={[
					{p: kp, name: 'lojjkli', talking: kTalk},
					...npcs.filter((n) => !n.gone).map((n) => ({p: n.pos, name: HATERS[n.j].name, bubble: bubbleOf(HATERS[n.j].name, t)})),
				]}
			/>
			<GameUI t={t} talking={kTalk} mode="plain" chatFrom={7} stick={walking ? [0, -walkAmt] : [0, 0]} />
			<CrackOverlay t={t} at={11.6} dur={3.0} />
			<BigText t={t} from={14.6} to={16.5} text="SQUEAK LEVEL: 9000 🐭" color="#ffd84d" top={470} size={100} />
			{t >= 24.6 ? <DisconnectDialog t={t - 24.6} message="You were kicked from this experience: Voice too squeaky." code="267" /> : null}
			<Fade t={t} inAt={t0} outFrom={30.4} outTo={31} />
		</AbsoluteFill>
	);
};

// ================================================================ broke in a box (+ myninn)
const BOX: V3 = [0, 0, 0];
const KLI_SIT: V3 = [0, 0, -0.2];
const HAND: V3 = [1.5, 2.85, 1.9]; // right hand, sitting + pointing forward
const MORNING: Env = {
	skyTop: '#5b7fd6',
	skyHorizon: '#ffc79a',
	sunDir: [0.6, 0.35, 0.7],
	sunColor: '#ffd2a1',
	sunIntensity: 2.3,
	hemiSky: '#ffe2c8',
	hemiGround: '#4a4048',
	hemiIntensity: 0.9,
	fog: ['#f2c6a8', 60, 260],
	sunGlow: 1.2,
};

const pigeonPath = (t: number): {p: V3; yaw: number} => {
	if (t < 44.8) {
		const k = range(t, 43.8, 44.8);
		return {p: lerp3([-14, 9, 8], [HAND[0], HAND[1] + 0.4, HAND[2]], ease(k)), yaw: Math.PI / 2};
	}
	const k = range(t, 44.8, 46.4);
	return {p: lerp3([HAND[0], HAND[1] + 0.4, HAND[2]], [16, 12, -6], ease(k)), yaw: Math.PI * 0.75};
};

const POOR_SHOTS: Shot[] = [
	{from: 31, to: 34.4, cam: (t, k) => ({pos: lerp3([9, 15, 22], [5, 6.5, 13], ease(k)), target: [0, 2, 0], fov: 46})},
	{from: 34.4, to: 36.6, cam: (t, k) => ({pos: lerp3([0.4, 3.9, 6.0], [0.3, 3.85, 5.2], k), target: [0, 3.6, 0], fov: 40})},
	{from: 36.6, to: 42.0, cam: (t, k) => ({pos: lerp3([1.6, 3.8, 8.0], [1.3, 3.7, 7.2], k), target: [0, 2.9, 0.8], fov: 44})},
	{from: 42.0, to: 43.8, cam: (t, k) => ({pos: lerp3([1.8, 3.7, 6.2], [1.6, 3.6, 5.6], k), target: [0.6, 3.0, 0.8], fov: 42})},
	{from: 43.8, to: 47.6, cam: (t, k) => ({pos: lerp3([6, 5, 12], [5, 5.5, 12.5], k), target: [0, 3.5, 1], fov: 50})},
	{from: 47.6, to: 49.4, cam: (t, k) => ({pos: lerp3([0.3, 3.6, 4.2], [0.2, 30, 7], ease(range(t, 47.75, 48.6))), target: [0, 2.8, 0], fov: 46})},
	{from: 49.4, to: 55, cam: (t, k) => ({pos: lerp3([-10, 5, 12], [-7, 4.2, 9.5], k), target: [0, 2.4, 0], fov: 46})},
];

const M_FROM: V3 = [14, 0, 8];
const M_TO: V3 = [3.6, 0, 6.5];
const myPos = (t: number): V3 => lerp3(M_FROM, M_TO, range(t, 56.0, 58.4));
const MY_SHOTS: Shot[] = [
	{from: 55, to: 58.6, cam: (t, k) => ({pos: lerp3([4, 6.5, 20], [3, 5.8, 18], k), target: [1.5, 3, 3], fov: 46})},
	{from: 58.6, to: 59.9, cam: () => ({pos: [M_TO[0] - 2.6, 5.4, M_TO[2] - 2.6], target: [M_TO[0], 4.6, M_TO[2]], fov: 42})},
	{from: 59.9, to: 62.6, cam: (t, k) => ({pos: lerp3([7.8, 6.2, 9.0], [7.2, 6.0, 8.4], k), target: [0, 3.2, 0], fov: 40})},
	{from: 62.6, to: 64.2, cam: (t, k) => ({pos: [-0.6, 3.9, 5.2 - k * 0.3], target: [0, 3.65, 0], fov: 40})},
	{from: 64.2, to: 67.4, cam: (t, k) => ({pos: lerp3([2.3, 4.9, 2.6], [2.5, 4.9, 3.1], k), target: [M_TO[0], 4.6, M_TO[2]], fov: 42})},
	{from: 67.4, to: 68.5, cam: () => ({pos: [-0.6, 3.9, 4.9], target: [0, 3.65, 0], fov: 40})},
	{from: 68.5, to: 74, cam: (t, k) => ({pos: lerp3([-6, 5.5, 15], [-5, 5.5, 13.5], k), target: [1.6, 3, 2.5], fov: 46})},
];

const HairSign: React.FC = () => {
	const tex = signTexture('HAIR 4 SALE: 1 R$', '#f2dfb4', '#2a1608', 'hairsign');
	return (
		<mesh position={[0, 2.5, 2.1]} rotation={[-0.1, 0, 0]}>
			<planeGeometry args={[3.2, 0.8]} />
			<meshStandardMaterial map={tex} />
		</mesh>
	);
};

export const AlleyScene: React.FC<{t0: number; mode: 'poor' | 'myninn'}> = ({t0, mode}) => {
	const t = t0 + useCurrentFrame() / FPS;
	const poor = mode === 'poor';
	const base = shotAt(poor ? POOR_SHOTS : MY_SHOTS, t).cam;
	const cam = withShake(base, t, t > 47.8 && t < 48.6 ? 0.1 : 0);
	const flash = t > 47.8 && t < 48.2 ? 1 - (t - 47.8) / 0.4 : 0;
	const env = poor ? {...LOBBY_NIGHT, sunIntensity: LOBBY_NIGHT.sunIntensity + flash * 4} : lerpEnv(LOBBY_NIGHT, MORNING, range(t, 55, 57));
	const kTalk = talking('kli', t);
	const card = !poor && t >= 58.6 && t < 59.9;
	const tv = card ? 58.6 : t;
	// kli
	let kFace: string = 'sad';
	if (poor && t > 35.2) kFace = 'blank';
	if (poor && t > 41.8) kFace = 'happy';
	if (poor && t > 44.8) kFace = 'shock';
	if (poor && t > 47.6) kFace = 'blank';
	if (!poor) kFace = tv > 64.2 ? (tv > 68.5 ? 'happy' : 'worried') : 'blank';
	const getUp = poor ? 0 : range(tv, 71.6, 72.2);
	const hop = !poor && tv > 71.9 && tv < 72.6 ? Math.sin(((tv - 71.9) / 0.7) * Math.PI) * 2.2 : 0;
	const holdingBread = poor && t > 41.8 && t < 44.8;
	const pg = poor ? pigeonPath(t) : null;
	const my = myPos(tv);
	const myWalk = tv > 56 && tv < 58.4;
	return (
		<AbsoluteFill>
			<Stage cam={cam} env={{...env, shadowCenter: [0, 0, 2], shadowSize: 22}}>
				<Alley wet={poor ? 1 : 0.6} />
				{poor ? <Rain t={t} center={[0, 0, 4]} area={40} count={900} /> : null}
				<pointLight position={[3, 6, 5]} color={poor ? '#9fb6ff' : '#ffd2a1'} intensity={poor ? 28 : 10} distance={14} decay={1.5} />
				<CardboardBox position={BOX} />
				<Avatar
					look={{...NOOB_KLI, face: kFace as never}}
					position={[KLI_SIT[0], KLI_SIT[1], KLI_SIT[2] + getUp * 2]}
					rotationY={!poor && tv > 59.9 && tv < 71.6 ? 0.45 : 0}
					pose={{
						time: tv,
						sit: 1 - getUp,
						jump: hop,
						armsUp: hop > 0 ? 0.7 : t > 47.6 && t < 48.4 ? 1 : 0,
						point: holdingBread ? 1 : 0,
						headPitch: poor && t > 49 ? 0.3 : 0,
					}}
				/>
				{poor && t > 36.6 && t < 42 ? <HairSign /> : null}
				{holdingBread ? <Bread position={HAND} rotationY={0.3} /> : null}
				{pg && t > 43.8 && t < 46.4 ? (
					<group>
						<Pigeon position={pg.p} rotationY={pg.yaw} t={t} scale={2} />
						{t >= 44.8 ? <Bread position={[pg.p[0], pg.p[1] - 0.5, pg.p[2]]} scale={0.8} /> : null}
					</group>
				) : null}
				{poor && t > 35.2 && t < 36.2 ? (
					<Sparkles points={new Array(10).fill(0).map((_, i) => [Math.sin(i) * 0.8, 3.4 + (t - 35.2) * 2 + rand(i) * 0.5, 0.8 + Math.cos(i) * 0.4] as V3)} t={t} color="#ffffff" size={0.12} />
				) : null}
				{!poor ? (
					<Avatar look={MYNINN_LOOK} position={my} rotationY={face(my, [0, 0, 0])} pose={{time: tv + 2, walk: tv * 9, walkAmt: myWalk ? 1 : 0, point: tv > 64.2 && tv < 66.8 ? 1 : 0, wave: tv > 58.4 && tv < 59.6 ? 1 : 0}} />
				) : null}
			</Stage>
			<Billboards
				cam={cam}
				t={t}
				items={[
					{p: [KLI_SIT[0], -1, KLI_SIT[2]], name: 'lojjkli', talking: kTalk},
					...(!poor ? [{p: my, name: 'myninn', talking: talking('myninn', tv)}] : []),
				]}
			/>
			<GameUI t={t} talking={kTalk} mode="plain" chatFrom={poor ? 40 : 999} />
			<RobuxCounter value={0} pulse={poor && t > 32.3 && t < 32.6 ? 1 : 0} />
			{poor ? <AbsoluteFill style={{background: '#1b2a4a', mixBlendMode: 'multiply', opacity: 0.3}} /> : null}
			<Flash t={t} at={47.8} dur={0.35} />
			{poor ? <BigText t={t} from={39.3} to={41.0} text="💇 HAIR 4 SALE: 1 R$" color="#ffd84d" top={470} size={90} /> : null}
			{poor ? <BigText t={t} from={47.6} to={49.2} text="WHY?!" color="#ff5b5b" top={140} size={140} /> : null}
			{!poor ? (
				<>
					<FreezeTint on={card} color="rgba(40,255,220,0.16)" />
					<NameCard t={t} at={58.6} dur={1.3} name="MYNINN" sub="THE FRIEND WITH A PLAN" color="#5fe3d2" />
					<BigText t={t} from={65.8} to={67.9} text="ROBLOX STUDIO ✨" color="#7fd0ff" top={150} />
					<PopWords
						t={t}
						until={71.6}
						words={[
							{at: 68.6, text: 'MAKE GAMES 🎮', x: 520, y: 300, rot: -6},
							{at: 69.6, text: 'MAKE MONEY 💸', x: 1400, y: 420, rot: 5, color: '#7cff8a'},
							{at: 70.5, text: 'GET RICH 🤑', x: 960, y: 640, rot: -3, color: '#ffd84d'},
						]}
					/>
				</>
			) : null}
			<Fade t={t} inAt={t0} inDur={0.6} outFrom={poor ? 54.4 : 73.6} outTo={poor ? 55 : 74} />
		</AbsoluteFill>
	);
};
