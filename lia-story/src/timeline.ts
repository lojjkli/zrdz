import voices from './voices.json';

export const FPS = 30;
export const W = 1920;
export const H = 1080;
export const f = (sec: number) => Math.round(sec * FPS);

// Scene boundaries in seconds.
export const SCENES = {
	cold: [0, 7.5],
	app: [7.5, 14],
	lobby: [14, 27.6],
	role: [27.6, 30.6],
	mansion: [30.6, 72],
	sad: [72, 84],
	arrival: [84, 96.4],
	love: [96.4, 110],
	party: [110, 123.6],
	space: [123.6, 127.4],
	disconnect: [127.4, 131.4],
	end: [131.4, 140],
} as const;

export const TOTAL = f(SCENES.end[1]);

export type VoiceId = keyof typeof voices;
export type Speaker = 'narr' | 'lia' | 'req' | 'kli' | 'yf' | 'boomp' | 'crowd';

export const speakerOf = (id: VoiceId): Speaker =>
	(({n: 'narr', l: 'lia', r: 'req', k: 'kli', y: 'yf', b: 'boomp'}) as Record<string, Speaker>)[id[0]] ?? 'crowd';

export const SPEAKER_TAG: Record<Speaker, [string, string] | null> = {
	narr: null,
	crowd: null,
	lia: ['Lia', '#ff8fd0'],
	req: ['REQ', '#ffd23f'],
	kli: ['kli', '#b9b9ff'],
	yf: ['YF', '#ff6b6b'],
	boomp: ['BoompjeJunior', '#d59bff'],
};

export const VOICE_CUES: {id: VoiceId; at: number; vol?: number}[] = [
	{id: 'n_intro', at: 1.0},
	{id: 'n_loved', at: 3.0},
	{id: 'n_mm2', at: 8.0},
	{id: 'n_friends', at: 14.8},
	{id: 'n_req', at: 18.0},
	{id: 'n_mikey', at: 19.2},
	{id: 'n_ade', at: 20.4},
	{id: 'l_round', at: 22.2},
	{id: 'r_bring', at: 25.9},
	{id: 'n_met', at: 31.0},
	{id: 'l_cute', at: 34.2},
	{id: 'n_thought', at: 38.0},
	{id: 'n_mic', at: 40.8},
	{id: 'k_wsg', at: 43.6},
	{id: 'k_girl', at: 46.4},
	{id: 'l_what', at: 49.4},
	{id: 'n_eboy', at: 50.6},
	{id: 'k_yf', at: 55.2},
	{id: 'y_trash', at: 59.2},
	{id: 'y_lia', at: 61.6},
	{id: 'n_mean', at: 64.0},
	{id: 'y_out', at: 67.0},
	{id: 'n_gone', at: 72.6},
	{id: 'l_cry', at: 76.4},
	{id: 'n_nolove', at: 78.6},
	{id: 'n_but', at: 82.4},
	{id: 'n_boomp', at: 85.6},
	{id: 'n_lives', at: 89.4},
	{id: 'b_hoi', at: 92.8},
	{id: 'l_oh', at: 95.2},
	{id: 'n_love', at: 96.8},
	{id: 'l_kids', at: 99.8},
	{id: 'b_many', at: 101.2},
	{id: 'l_67', at: 102.6},
	{id: 'c_67', at: 104.4, vol: 0.8},
	{id: 'c_67b', at: 104.9, vol: 0.7},
	{id: 'n_67', at: 106.8},
	{id: 'n_perfect', at: 110.4},
	{id: 'r_feel', at: 113.0},
	{id: 'k_bro', at: 117.6},
	{id: 's_ew', at: 118.7, vol: 0.7},
	{id: 'n_fart', at: 119.4},
	{id: 's_aah1', at: 120.9, vol: 0.55},
	{id: 's_noo', at: 121.3, vol: 0.5},
	{id: 'n_explode', at: 121.5},
	{id: 's_aah2', at: 122.4, vol: 0.5},
	{id: 'r_mybad', at: 129.2},
	{id: 'n_soon', at: 133.0},
	{id: 'k_post', at: 137.4},
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
	| 'role' | 'join' | 'leave' | 'door' | 'gas' | 'choir' | 'heartbeat' | 'rain' | 'freeze' | 'bigboom';

// Taps on the screen (also drive the touch indicator): [sec, x, y]
export const TAPS: [number, number, number][] = [
	[9.2, 474, 342], // MM2 tile on home
	[11.4, 1460, 610], // Play button
];

// When each kid pops in (67 of them)
export const KID_POP = (i: number) => 104.0 + Math.pow(i / 66, 0.8) * 2.4;

export const SFX_CUES: {id: Sfx; at: number; vol?: number; dur?: number}[] = [
	// cold open
	{id: 'braam', at: 0.2, vol: 0.5},
	{id: 'riser', at: 4.6, vol: 0.35},
	// app
	...TAPS.map(([at]) => ({id: 'tap' as Sfx, at, vol: 0.6})),
	{id: 'pop', at: 9.3, vol: 0.4},
	{id: 'pop', at: 11.5, vol: 0.4},
	// lobby
	{id: 'join', at: 14.5, vol: 0.4},
	{id: 'steps', at: 15.2, vol: 0.3},
	{id: 'freeze', at: 18.0, vol: 0.55},
	{id: 'freeze', at: 19.2, vol: 0.55},
	{id: 'freeze', at: 20.4, vol: 0.55},
	{id: 'join', at: 25.6, vol: 0.35},
	// role reveal
	{id: 'role', at: 27.6, vol: 0.75},
	// mansion
	{id: 'steps', at: 31.2, vol: 0.25},
	{id: 'chat', at: 35.0, vol: 0.3},
	{id: 'chat', at: 36.2, vol: 0.3},
	{id: 'riser', at: 40.6, vol: 0.3},
	{id: 'scratch', at: 42.9, vol: 0.55},
	{id: 'vineboom', at: 43.6, vol: 0.9},
	{id: 'vineboom', at: 49.4, vol: 0.6},
	{id: 'chat', at: 45.4, vol: 0.3},
	{id: 'chat', at: 45.9, vol: 0.3},
	{id: 'chat', at: 46.3, vol: 0.3},
	{id: 'join', at: 57.0, vol: 0.4},
	{id: 'door', at: 56.9, vol: 0.55},
	{id: 'chat', at: 60.2, vol: 0.3},
	{id: 'chat', at: 62.6, vol: 0.3},
	{id: 'chat', at: 63.1, vol: 0.3},
	{id: 'chat', at: 63.7, vol: 0.3},
	{id: 'leave', at: 68.8, vol: 0.45},
	{id: 'door', at: 68.0, vol: 0.4},
	{id: 'leave', at: 69.8, vol: 0.4},
	{id: 'leave', at: 70.6, vol: 0.4},
	{id: 'leave', at: 71.2, vol: 0.4},
	{id: 'leave', at: 71.6, vol: 0.4},
	// sad
	{id: 'rain', at: 72.0, vol: 0.35, dur: 12.4},
	{id: 'rumble', at: 74.0, vol: 0.35},
	// arrival
	{id: 'join', at: 84.0, vol: 0.45},
	{id: 'choir', at: 84.0, vol: 0.55},
	{id: 'sparkle', at: 84.2, vol: 0.4},
	{id: 'whoosh', at: 86.6, vol: 0.4},
	{id: 'whoosh', at: 87.4, vol: 0.4},
	{id: 'whoosh', at: 88.1, vol: 0.4},
	{id: 'pop', at: 90.6, vol: 0.35},
	{id: 'heartbeat', at: 95.0, vol: 0.8},
	{id: 'heartpop', at: 95.4, vol: 0.45},
	// love
	{id: 'sparkle', at: 96.6, vol: 0.4},
	{id: 'heartpop', at: 97.0, vol: 0.4},
	{id: 'scratch', at: 102.5, vol: 0.4},
	{id: 'vineboom', at: 103.28, vol: 0.7},
	...new Array(67).fill(0).filter((_, i) => i % 3 === 0).map((_, k) => ({id: 'pop' as Sfx, at: KID_POP(k * 3), vol: 0.32})),
	{id: 'cheer', at: 104.6, vol: 0.4},
	// party
	{id: 'scratch', at: 114.6, vol: 0.5},
	{id: 'fart', at: 115.2, vol: 0.95},
	{id: 'vineboom', at: 117.6, vol: 0.7},
	{id: 'gas', at: 118.6, vol: 0.6},
	{id: 'rumble', at: 119.0, vol: 0.8},
	{id: 'siren', at: 119.4, vol: 0.12, dur: 4.2},
	{id: 'riser', at: 120.6, vol: 0.5},
	{id: 'crack', at: 122.6, vol: 0.6},
	// space
	{id: 'bigboom', at: 124.4, vol: 1.0},
	// disconnect + end
	{id: 'disconnect', at: 127.6, vol: 0.5},
	{id: 'braam', at: 131.6, vol: 0.6},
	{id: 'vineboom', at: 137.4, vol: 0.5},
];

export const MUSIC_CUES: {id: string; from: number; to: number; vol: number; fadeIn?: number; fadeOut?: number; offset?: number}[] = [
	{id: 'intro', from: 0, to: 7.8, vol: 0.5, fadeOut: 0.8},
	{id: 'lobby', from: 7.5, to: 27.7, vol: 0.3, fadeIn: 0.4, fadeOut: 0.3},
	{id: 'mystery', from: 30.4, to: 42.95, vol: 0.32, fadeIn: 0.4, fadeOut: 0.05},
	{id: 'mystery', from: 50.4, to: 72.2, vol: 0.26, fadeIn: 1.0, fadeOut: 0.8, offset: 4},
	{id: 'sad', from: 72.2, to: 83.2, vol: 0.45, fadeIn: 0.6, fadeOut: 1.2},
	{id: 'romance', from: 84.3, to: 104.0, vol: 0.36, fadeIn: 1.2, fadeOut: 0.2},
	{id: 'party', from: 104.0, to: 114.6, vol: 0.3, fadeIn: 0.05, fadeOut: 0.05},
	{id: 'chaos', from: 119.0, to: 124.3, vol: 0.42, fadeIn: 0.2, fadeOut: 0.05},
	{id: 'sad', from: 127.6, to: 131.4, vol: 0.3, fadeIn: 0.8, fadeOut: 0.8, offset: 2},
	{id: 'intro', from: 131.4, to: 136.6, vol: 0.45, fadeIn: 0.2, fadeOut: 1.4, offset: 3.0},
];

export type ChatLine = {at: number; name: string; text: string; color?: string; system?: boolean};

export const C = {
	lia: '#ff7ad0',
	req: '#ffd166',
	mikey: '#7ad3ff',
	ade: '#9cff8a',
	kli: '#c7c7ff',
	yf: '#ff6b6b',
	boomp: '#d59bff',
};

export const CHAT: ChatLine[] = [
	{at: 14.6, name: '', text: 'Lia has joined the experience.', system: true},
	{at: 16.0, name: 'Mikey', text: 'LIA!! 👋', color: C.mikey},
	{at: 16.9, name: 'Ade', text: 'hiii lia', color: C.ade},
	{at: 20.9, name: 'REQ', text: 'yo', color: C.req},
	{at: 25.7, name: '', text: 'lojjkli has joined the experience.', system: true},
	{at: 32.5, name: 'Mikey', text: 'who is that', color: C.mikey},
	{at: 35.0, name: 'Mikey', text: 'hi bestie 💅', color: C.mikey},
	{at: 36.2, name: 'Ade', text: 'ur fit is so cute girl', color: C.ade},
	{at: 37.8, name: 'lojjkli', text: ':)', color: C.kli},
	{at: 45.4, name: 'Mikey', text: 'BRO 💀💀💀', color: C.mikey},
	{at: 45.9, name: 'Ade', text: 'HIS VOICE 😭', color: C.ade},
	{at: 46.3, name: 'REQ', text: 'my phone is vibrating', color: C.req},
	{at: 48.0, name: 'Mikey', text: 'deeper than the ocean', color: C.mikey},
	{at: 57.0, name: '', text: 'YF has joined the experience.', system: true},
	{at: 60.2, name: 'YF', text: '########## lol', color: C.yf},
	{at: 62.6, name: 'YF', text: 'ur all ######', color: C.yf},
	{at: 63.1, name: 'Mikey', text: 'bro chill', color: C.mikey},
	{at: 63.7, name: 'Ade', text: 'why r u so mean', color: C.ade},
	{at: 68.8, name: '', text: 'YF has left the experience.', system: true},
	{at: 69.4, name: 'Mikey', text: 'gtg dinner', color: C.mikey},
	{at: 69.8, name: '', text: 'Mikey has left the experience.', system: true},
	{at: 70.6, name: '', text: 'Ade has left the experience.', system: true},
	{at: 71.2, name: '', text: 'REQ has left the experience.', system: true},
	{at: 71.6, name: '', text: 'lojjkli has left the experience.', system: true},
	{at: 84.0, name: '', text: 'BoompjeJunior has joined the experience.', system: true},
	{at: 91.0, name: 'BoompjeJunior', text: 'i live 20 min away btw', color: C.boomp},
	{at: 97.6, name: 'Lia', text: '🥺💕', color: C.lia},
	{at: 104.4, name: 'BoompjeJunior', text: 'SIX SEVENNN', color: C.boomp},
	{at: 105.8, name: 'Lia', text: '67 💀💀', color: C.lia},
	{at: 108.6, name: '', text: 'REQ has joined the experience.', system: true},
	{at: 108.9, name: '', text: 'Mikey has joined the experience.', system: true},
	{at: 109.2, name: '', text: 'Ade has joined the experience.', system: true},
	{at: 109.5, name: '', text: 'lojjkli has joined the experience.', system: true},
	{at: 111.0, name: 'Mikey', text: 'WHY ARE THERE 67 KIDS', color: C.mikey},
	{at: 112.0, name: 'Ade', text: 'congrats lia 😭', color: C.ade},
	{at: 116.6, name: 'Mikey', text: 'REQ NO', color: C.mikey},
	{at: 117.2, name: 'Ade', text: '🤢🤢🤢', color: C.ade},
	{at: 118.3, name: 'BoompjeJunior', text: 'bro what did u eat', color: C.boomp},
	{at: 120.2, name: 'Mikey', text: 'RUNNNN', color: C.mikey},
	{at: 121.2, name: 'Lia', text: 'MY KIDS 😭', color: C.lia},
];

export const bubbleOf = (name: string, t: number) => {
	const b = [...CHAT].reverse().find((c) => c.name === name && t >= c.at && t < c.at + 2.6);
	return b ? {text: b.text, age: t - b.at} : null;
};
