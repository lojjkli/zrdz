import voices from './voices.json';

export const FPS = 24;
export const W = 1920;
export const H = 1080;
export const f = (sec: number) => Math.round(sec * FPS);

// Scene boundaries in seconds.
export const SCENES = {
	cold: [0, 7],
	squeak: [7, 31],
	poor: [31, 55],
	myninn: [55, 74],
	studio: [74, 100],
	blender: [100, 126],
	rich: [126, 152],
	donut: [152, 168],
	end: [168, 180],
} as const;

export const TOTAL = f(SCENES.end[1]);

export type VoiceId = keyof typeof voices;
export type Speaker = 'narr' | 'kli' | 'myninn' | 'crowd' | 'sfx';

export const speakerOf = (id: VoiceId): Speaker =>
	(({n: 'narr', k: 'kli', m: 'myninn', c: 'crowd', s: 'sfx'}) as Record<string, Speaker>)[id[0]] ?? 'sfx';

export const SPEAKER_TAG: Record<Speaker, [string, string] | null> = {
	narr: null,
	sfx: null,
	crowd: ['Everyone', '#ffb3b3'],
	kli: ['kli', '#b9b9ff'],
	myninn: ['myninn', '#5fe3d2'],
};

// kli's voice drops when lightning hits him
export const VOICE_DROP = 115.0;

export const VOICE_CUES: {id: VoiceId; at: number; vol?: number}[] = [
	{id: 'n_intro', at: 0.9},
	{id: 'n_problem', at: 2.8},
	// squeak
	{id: 'k_hi', at: 9.8},
	{id: 'n_squeak', at: 13.6},
	{id: 'k_please', at: 16.8},
	{id: 'c_ew', at: 18.6, vol: 0.9},
	{id: 'n_hated', at: 26.0},
	// poor
	{id: 'n_poor', at: 32.0},
	{id: 'n_sell', at: 36.6},
	{id: 'k_hair', at: 39.2},
	{id: 'k_bread', at: 42.2},
	{id: 'n_pigeon', at: 44.6},
	{id: 'k_why', at: 47.6},
	{id: 'n_lowest', at: 49.4},
	// myninn
	{id: 'n_then', at: 55.6},
	{id: 'm_box', at: 60.2},
	{id: 'k_poor', at: 62.8},
	{id: 'm_studio', at: 64.2},
	{id: 'k_whats', at: 67.4},
	{id: 'm_make', at: 68.5},
	{id: 'k_lets', at: 71.8},
	// studio
	{id: 'n_started', at: 74.6},
	{id: 'n_bad', at: 78.0},
	{id: 'k_oops', at: 81.6},
	{id: 'n_baseplate', at: 83.2},
	{id: 'n_dislike', at: 86.6},
	{id: 's_oof', at: 94.3},
	{id: 'k_giveup', at: 96.6},
	// blender
	{id: 'n_met', at: 102.8},
	{id: 'k_cube', at: 106.4},
	{id: 'n_love', at: 108.4},
	{id: 'n_changed', at: 111.2},
	{id: 'k_wsg', at: 116.2},
	{id: 'n_deepest', at: 118.4},
	{id: 'n_glaze', at: 122.3},
	// rich
	{id: 'n_donut', at: 126.6},
	{id: 'n_models', at: 129.0},
	{id: 'k_rich', at: 133.6},
	{id: 'c_please', at: 137.8, vol: 0.9},
	{id: 'k_nah', at: 139.8},
	{id: 'n_richest', at: 141.4},
	{id: 'm_welcome', at: 146.0},
	{id: 'k_thanks', at: 148.2},
	// donut
	{id: 'n_forgot', at: 152.4},
	{id: 'n_physics', at: 154.6},
	{id: 's_aah1', at: 158.0, vol: 0.6},
	{id: 's_aah2', at: 158.6, vol: 0.55},
	{id: 'k_bro', at: 161.0},
	// end
	{id: 'n_soon', at: 170.6},
	{id: 'k_post', at: 175.4},
	{id: 'k_jk', at: 177.2},
];

export const voiceSec = (id: VoiceId) => voices[id].sec;
export const voiceText = (id: VoiceId) => voices[id].text;
export const voiceFile = (id: VoiceId) => voices[id].file;

// Is this speaker talking on voice chat at time t (sec)? Used for mic indicators.
export const talking = (who: Speaker, t: number) =>
	VOICE_CUES.some((c) => speakerOf(c.id) === who && t >= c.at && t <= c.at + voiceSec(c.id) - 0.05);

export type Sfx =
	| 'tap' | 'pop' | 'chat' | 'whoosh' | 'sparkle' | 'cheer' | 'rumble' | 'boom' | 'crack' | 'siren'
	| 'disconnect' | 'braam' | 'riser' | 'scratch' | 'land' | 'heartpop' | 'steps' | 'fart' | 'vineboom'
	| 'role' | 'join' | 'leave' | 'door' | 'gas' | 'choir' | 'heartbeat' | 'rain' | 'freeze' | 'bigboom'
	| 'purchase' | 'win' | 'lose' | 'diamond' | 'buzz' | 'bells' | 'meteor' | 'reel';

// Taps on the screen (also drive the touch indicator): [sec, x, y]
export const TAPS: [number, number, number][] = [];

export const LEAVES = [20.4, 20.9, 21.4, 21.9];
export const PARTS_DROP = (i: number) => 75.6 + i * 0.45;

export const SFX_CUES: {id: Sfx; at: number; vol?: number; dur?: number}[] = [
	// cold
	{id: 'braam', at: 0.2, vol: 0.5},
	{id: 'riser', at: 4.4, vol: 0.3},
	// squeak
	{id: 'join', at: 7.1, vol: 0.4},
	{id: 'steps', at: 7.3, vol: 0.3},
	{id: 'chat', at: 8.2, vol: 0.3},
	{id: 'chat', at: 8.9, vol: 0.3},
	{id: 'scratch', at: 11.45, vol: 0.6},
	{id: 'crack', at: 11.6, vol: 0.8},
	{id: 'chat', at: 11.9, vol: 0.3},
	{id: 'chat', at: 12.5, vol: 0.3},
	{id: 'chat', at: 13.1, vol: 0.3},
	{id: 'vineboom', at: 14.6, vol: 0.7},
	...LEAVES.map((at) => ({id: 'leave' as Sfx, at, vol: 0.45})),
	{id: 'disconnect', at: 24.6, vol: 0.5},
	// poor
	{id: 'rain', at: 31.0, vol: 0.35, dur: 24},
	{id: 'rumble', at: 32.4, vol: 0.3},
	{id: 'pop', at: 35.2, vol: 0.6},
	{id: 'chat', at: 40.9, vol: 0.3},
	{id: 'chat', at: 41.4, vol: 0.3},
	{id: 'whoosh', at: 43.9, vol: 0.5},
	{id: 'pop', at: 44.8, vol: 0.5},
	{id: 'whoosh', at: 45.3, vol: 0.45},
	{id: 'boom', at: 47.8, vol: 0.7},
	{id: 'rumble', at: 47.9, vol: 0.7},
	// myninn
	{id: 'steps', at: 56.0, vol: 0.3},
	{id: 'sparkle', at: 65.8, vol: 0.45},
	{id: 'pop', at: 68.6, vol: 0.45},
	{id: 'pop', at: 69.6, vol: 0.45},
	{id: 'purchase', at: 70.5, vol: 0.45},
	{id: 'cheer', at: 72.0, vol: 0.35},
	// studio
	...new Array(8).fill(0).map((_, i) => ({id: 'land' as Sfx, at: PARTS_DROP(i) + 0.35, vol: 0.3})),
	{id: 'buzz', at: 79.2, vol: 0.35},
	{id: 'buzz', at: 80.4, vol: 0.35},
	{id: 'boom', at: 82.3, vol: 0.7},
	{id: 'leave', at: 83.8, vol: 0.5},
	{id: 'whoosh', at: 86.0, vol: 0.4},
	{id: 'pop', at: 89.6, vol: 0.5},
	{id: 'lose', at: 89.8, vol: 0.4},
	{id: 'steps', at: 92.4, vol: 0.25},
	{id: 'whoosh', at: 93.3, vol: 0.4},
	// blender
	{id: 'riser', at: 100.4, vol: 0.35},
	{id: 'choir', at: 101.0, vol: 0.55},
	{id: 'meteor', at: 101.2, vol: 0.4},
	{id: 'land', at: 102.6, vol: 0.7},
	{id: 'sparkle', at: 102.7, vol: 0.4},
	{id: 'tap', at: 106.2, vol: 0.5},
	{id: 'pop', at: 107.6, vol: 0.6},
	{id: 'heartbeat', at: 108.2, vol: 0.8},
	{id: 'heartpop', at: 108.6, vol: 0.45},
	{id: 'scratch', at: 111.0, vol: 0.5},
	{id: 'rumble', at: 111.4, vol: 0.6},
	{id: 'riser', at: 112.6, vol: 0.45},
	{id: 'boom', at: VOICE_DROP, vol: 1.0},
	{id: 'bigboom', at: VOICE_DROP, vol: 0.5},
	{id: 'vineboom', at: 116.2, vol: 0.9},
	{id: 'crack', at: 116.4, vol: 0.8},
	{id: 'chat', at: 119.0, vol: 0.3},
	{id: 'chat', at: 119.6, vol: 0.3},
	{id: 'chat', at: 120.2, vol: 0.3},
	{id: 'pop', at: 122.4, vol: 0.5},
	{id: 'pop', at: 123.2, vol: 0.5},
	{id: 'vineboom', at: 124.0, vol: 0.6},
	// rich
	{id: 'sparkle', at: 127.4, vol: 0.45},
	{id: 'purchase', at: 129.4, vol: 0.4},
	{id: 'diamond', at: 130.4, vol: 0.4},
	{id: 'purchase', at: 131.4, vol: 0.4},
	{id: 'win', at: 132.6, vol: 0.4},
	{id: 'steps', at: 136.4, vol: 0.35},
	{id: 'chat', at: 136.6, vol: 0.3},
	{id: 'chat', at: 137.1, vol: 0.3},
	{id: 'vineboom', at: 139.8, vol: 0.8},
	{id: 'bells', at: 141.6, vol: 0.4},
	{id: 'pop', at: 145.8, vol: 0.5},
	// donut
	{id: 'rumble', at: 155.8, vol: 0.6},
	{id: 'rumble', at: 157.6, vol: 0.8},
	{id: 'crack', at: 159.0, vol: 0.8},
	{id: 'boom', at: 159.1, vol: 0.6},
	{id: 'siren', at: 158.2, vol: 0.1, dur: 4.4},
	{id: 'bigboom', at: 163.2, vol: 0.9},
	{id: 'disconnect', at: 163.8, vol: 0.5},
	// end
	{id: 'braam', at: 168.2, vol: 0.6},
	{id: 'scratch', at: 176.2, vol: 0.5},
	{id: 'vineboom', at: 177.2, vol: 0.8},
];

export const MUSIC_CUES: {id: string; from: number; to: number; vol: number; fadeIn?: number; fadeOut?: number; offset?: number}[] = [
	{id: 'intro', from: 0, to: 7.2, vol: 0.5, fadeOut: 0.8},
	{id: 'lobby', from: 7.0, to: 11.45, vol: 0.3, fadeIn: 0.3, fadeOut: 0.05},
	{id: 'lobby', from: 13.6, to: 22.5, vol: 0.13, fadeIn: 1.0, fadeOut: 1.0, offset: 6},
	{id: 'sad', from: 24.6, to: 31, vol: 0.3, fadeIn: 1.0, fadeOut: 0.6},
	{id: 'sad', from: 31.4, to: 54.8, vol: 0.38, fadeIn: 1.0, fadeOut: 1.0, offset: 3},
	{id: 'lobby', from: 55.4, to: 73.9, vol: 0.24, fadeIn: 1.2, fadeOut: 0.6},
	{id: 'mystery', from: 74.0, to: 85.8, vol: 0.28, fadeIn: 0.4, fadeOut: 0.4},
	{id: 'sad', from: 86.0, to: 99.8, vol: 0.28, fadeIn: 0.6, fadeOut: 0.6, offset: 5},
	{id: 'romance', from: 102.6, to: 111.0, vol: 0.34, fadeIn: 0.8, fadeOut: 0.05},
	{id: 'chaos', from: 116.2, to: 125.6, vol: 0.32, fadeIn: 0.05, fadeOut: 1.0},
	{id: 'party', from: 126.2, to: 151.8, vol: 0.3, fadeIn: 0.4, fadeOut: 1.0},
	{id: 'chaos', from: 155.6, to: 163.2, vol: 0.4, fadeIn: 0.6, fadeOut: 0.05},
	{id: 'sad', from: 163.8, to: 168, vol: 0.3, fadeIn: 0.8, fadeOut: 0.6, offset: 2},
	{id: 'intro', from: 168.0, to: 174.2, vol: 0.45, fadeIn: 0.2, fadeOut: 1.2, offset: 3.0},
];

export type ChatLine = {at: number; name: string; text: string; color?: string; system?: boolean};

export const C = {
	kli: '#c7c7ff',
	myninn: '#5fe3d2',
	toast: '#ffd166',
	slasher: '#ff7a7a',
	lily: '#ff9ad5',
	kaiib: '#9cff8a',
	hachi: '#7ad3ff',
};

export const HATERS = [
	{name: 'Toast_YT', color: C.toast},
	{name: 'xXslasherXx', color: C.slasher},
	{name: 'Lilyy_bloom', color: C.lily},
	{name: 'kaiib', color: C.kaiib},
];

export const CHAT: ChatLine[] = [
	{at: 7.2, name: '', text: 'lojjkli has joined the experience.', system: true},
	{at: 8.2, name: 'Toast_YT', text: 'new guy 👀', color: C.toast},
	{at: 8.9, name: 'Lilyy_bloom', text: 'hiii', color: C.lily},
	{at: 11.9, name: 'xXslasherXx', text: 'WHO LET THE MOUSE IN', color: C.slasher},
	{at: 12.5, name: 'Lilyy_bloom', text: 'my ears 💀💀', color: C.lily},
	{at: 13.1, name: 'Toast_YT', text: 'mute him rn', color: C.toast},
	...HATERS.map((h, i) => ({at: LEAVES[i], name: '', text: `${h.name} has left the experience.`, system: true})),
	// poor
	{at: 40.9, name: 'Toast_YT', text: 'no.', color: C.toast},
	{at: 41.4, name: 'Lilyy_bloom', text: 'u dont even have hair 💀', color: C.lily},
	// blender
	{at: 119.0, name: 'Toast_YT', text: 'MY PHONE IS SHAKING 📳', color: C.toast},
	{at: 119.6, name: 'Lilyy_bloom', text: 'who is THAT 😳', color: C.lily},
	{at: 120.2, name: 'xXslasherXx', text: 'my speaker just exploded', color: C.slasher},
	// rich
	{at: 136.6, name: 'Toast_YT', text: 'KLI!! remember me?? 🥺', color: C.toast},
	{at: 137.1, name: 'xXslasherXx', text: 'we were always friends fr', color: C.slasher},
	{at: 140.6, name: 'Lilyy_bloom', text: 'NAH 💀💀💀', color: C.lily},
	{at: 141.0, name: 'kaiib', text: 'he cooked yall', color: C.kaiib},
];

export const bubbleOf = (name: string, t: number) => {
	const b = [...CHAT].reverse().find((c) => c.name === name && t >= c.at && t < c.at + 2.6);
	return b ? {text: b.text, age: t - b.at} : null;
};
