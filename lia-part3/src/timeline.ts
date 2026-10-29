import voices from './voices.json';

export const FPS = 30;
export const W = 1920;
export const H = 1080;
export const f = (sec: number) => Math.round(sec * FPS);

// Scene boundaries in seconds.
export const SCENES = {
	cold: [0, 9.5],
	home: [9.5, 23.4],
	rise: [23.4, 37.5],
	chase: [37.5, 60],
	sorry: [60, 74],
	fan: [74, 89],
	end: [89, 102],
} as const;

export const TOTAL = f(SCENES.end[1]);

export type VoiceId = keyof typeof voices;
export type Speaker = 'narr' | 'lia' | 'boomp' | 'kids' | 'mikey' | 'ade' | 'req' | 'kid' | 'kli' | 'donut' | 'pigeon' | 'mill' | 'sfx';

export const speakerOf = (id: VoiceId): Speaker =>
	(({n: 'narr', l: 'lia', b: 'boomp', c: 'kids', m: 'mikey', a: 'ade', r: 'req', x: 'kid', k: 'kli', d: 'donut', p: 'pigeon', w: 'mill', s: 'sfx'}) as Record<string, Speaker>)[id[0]] ?? 'sfx';

export const SPEAKER_TAG: Record<Speaker, [string, string] | null> = {
	narr: null,
	sfx: null,
	kids: ['Everyone', '#ffb3b3'],
	lia: ['Lia', '#ff9ad5'],
	boomp: ['BoompjeJunior', '#ff9f40'],
	mikey: ['Mikey', '#7ad1ff'],
	ade: ['Ade', '#9cff8a'],
	req: ['REQ', '#ff5b5b'],
	kid: ['Kid #67', '#ffd23f'],
	kli: ['lojjkli', '#b9b9ff'],
	donut: ['TheDonut', '#ff8fc8'],
	pigeon: ['THE PIGEON', '#a9b4c4'],
	mill: ['THE WINDMILL', '#ff6b4a'],
};

export const RISE = 24.0;
export const BOUNCE = 55.2;
export const FART = 76.6;
export const BLOW = 77.6;

export const VOICE_CUES: {id: VoiceId; at: number; vol?: number}[] = [
	{id: 'n_prev', at: 0.6},
	{id: 'n_morning', at: 10.0},
	{id: 'b_family', at: 13.6},
	{id: 'p_coo', at: 16.2},
	{id: 'l_sign', at: 18.2},
	{id: 'n_rumble', at: 20.4},
	{id: 'n_back', at: 23.6},
	{id: 'w_req', at: 28.0},
	{id: 'r_me', at: 29.8},
	{id: 'w_you', at: 31.2},
	{id: 'c_67', at: 34.0, vol: 0.9},
	{id: 'l_run', at: 36.0},
	{id: 'n_chase', at: 37.8},
	{id: 'r_spin', at: 42.4},
	{id: 'm_sorry', at: 44.4},
	{id: 'a_math', at: 46.4},
	{id: 'k_wsg', at: 49.8},
	{id: 'd_allow', at: 53.4},
	{id: 'd_ow', at: 55.6},
	{id: 'n_useless', at: 57.0},
	{id: 'r_sorry', at: 60.4},
	{id: 'w_flowers', at: 63.6},
	{id: 'r_tulips', at: 67.2},
	{id: 'n_friends', at: 69.4},
	{id: 'r_uhoh', at: 74.4},
	{id: 'c_again', at: 75.6, vol: 0.9},
	{id: 'n_blow', at: 77.8},
	{id: 'w_useful', at: 81.2},
	{id: 'l_normal', at: 85.2},
	{id: 'c_nope', at: 87.2, vol: 0.9},
	{id: 'n_end', at: 90.8},
	{id: 'l_69', at: 96.4},
	{id: 'd_mother', at: 99.6},
];

export const voiceSec = (id: VoiceId) => voices[id].sec;
export const voiceText = (id: VoiceId) => voices[id].text;
export const voiceFile = (id: VoiceId) => voices[id].file;

export const talking = (who: Speaker, t: number) =>
	VOICE_CUES.some((c) => speakerOf(c.id) === who && t >= c.at && t <= c.at + voiceSec(c.id) - 0.05);

export type Sfx =
	| 'tap' | 'pop' | 'chat' | 'whoosh' | 'sparkle' | 'cheer' | 'rumble' | 'boom' | 'crack' | 'siren'
	| 'disconnect' | 'braam' | 'riser' | 'scratch' | 'land' | 'heartpop' | 'steps' | 'fart' | 'vineboom'
	| 'role' | 'join' | 'leave' | 'door' | 'gas' | 'choir' | 'heartbeat' | 'rain' | 'freeze' | 'bigboom'
	| 'tinyfart' | 'purchase' | 'win' | 'lose' | 'diamond' | 'buzz' | 'bells' | 'meteor' | 'reel';

export const TAPS: [number, number, number][] = [];

export const SFX_CUES: {id: Sfx; at: number; vol?: number; dur?: number}[] = [
	{id: 'braam', at: 0.2, vol: 0.5},
	{id: 'riser', at: 3.4, vol: 0.35},
	{id: 'vineboom', at: 4.6, vol: 0.7},
	// home
	{id: 'bells', at: 13.4, vol: 0.3},
	{id: 'heartpop', at: 16.2, vol: 0.4},
	{id: 'rumble', at: 20.4, vol: 0.5},
	{id: 'rumble', at: 22.2, vol: 0.7},
	// rise
	{id: 'rumble', at: RISE, vol: 0.8},
	{id: 'crack', at: RISE + 0.4, vol: 0.5},
	{id: 'braam', at: 27.0, vol: 0.6},
	{id: 'vineboom', at: 27.2, vol: 0.8},
	{id: 'vineboom', at: 31.3, vol: 0.5},
	{id: 'vineboom', at: 32.1, vol: 0.7},
	{id: 'scratch', at: 33.8, vol: 0.4},
	{id: 'siren', at: 36.0, vol: 0.25, dur: 1.6},
	// chase
	...[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11].map((i) => ({id: 'land' as Sfx, at: 38.0 + i * 0.9, vol: 0.45})),
	{id: 'chat', at: 41.0, vol: 0.3},
	{id: 'whoosh', at: 49.6, vol: 0.6},
	{id: 'land', at: 51.0, vol: 0.6},
	{id: 'whoosh', at: 53.8, vol: 0.5},
	{id: 'pop', at: BOUNCE, vol: 0.8},
	{id: 'land', at: BOUNCE + 0.9, vol: 0.6},
	{id: 'chat', at: 57.6, vol: 0.3},
	// sorry
	{id: 'sparkle', at: 61.0, vol: 0.4},
	{id: 'heartpop', at: 64.6, vol: 0.5},
	{id: 'choir', at: 69.4, vol: 0.35},
	{id: 'chat', at: 71.0, vol: 0.3},
	// fan
	{id: 'scratch', at: 74.2, vol: 0.6},
	{id: 'fart', at: FART, vol: 0.7},
	{id: 'gas', at: FART + 0.2, vol: 0.5},
	{id: 'whoosh', at: BLOW + 0.6, vol: 0.8},
	{id: 'whoosh', at: BLOW + 1.6, vol: 0.8},
	{id: 'win', at: 81.0, vol: 0.4},
	{id: 'vineboom', at: 87.2, vol: 0.5},
	// end
	{id: 'braam', at: 89.2, vol: 0.6},
	{id: 'scratch', at: 99.4, vol: 0.4},
	{id: 'vineboom', at: 99.6, vol: 0.8},
];

export const MUSIC_CUES: {id: string; from: number; to: number; vol: number; fadeIn?: number; fadeOut?: number; offset?: number}[] = [
	{id: 'intro', from: 0, to: 9.7, vol: 0.5, fadeOut: 0.8},
	{id: 'romance', from: 9.7, to: 20.4, vol: 0.26, fadeIn: 0.8, fadeOut: 0.6, offset: 2},
	{id: 'mystery', from: 20.4, to: 37.4, vol: 0.32, fadeIn: 0.5, fadeOut: 0.2},
	{id: 'chaos', from: 37.5, to: 59.8, vol: 0.32, fadeIn: 0.05, fadeOut: 0.6},
	{id: 'romance', from: 62.6, to: 74.0, vol: 0.3, fadeIn: 0.8, fadeOut: 0.05, offset: 6},
	{id: 'party', from: 80.8, to: 88.8, vol: 0.3, fadeIn: 0.4, fadeOut: 0.6},
	{id: 'intro', from: 89.0, to: 94.8, vol: 0.45, fadeIn: 0.2, fadeOut: 1.0, offset: 3},
	{id: 'mystery', from: 95.2, to: 102, vol: 0.26, fadeIn: 0.5, fadeOut: 0.6, offset: 3},
];

export type ChatLine = {at: number; name: string; text: string; color?: string; system?: boolean};

export const CHAT: ChatLine[] = [
	{at: 41.0, name: 'Toast_YT', text: 'the windmill is COOKING him 💀', color: '#ffd166'},
	{at: 57.6, name: 'kaiib', text: 'donut took 0 damage to the windmill', color: '#9cff8a'},
	{at: 71.0, name: 'Emii5287', text: 'this is so wholesome 🥹', color: '#ff9ad5'},
	{at: 81.6, name: 'HachiMC', text: 'windmill main character fr', color: '#7ad1ff'},
];

export const bubbleOf = (name: string, t: number) => {
	const b = [...CHAT].reverse().find((c) => c.name === name && t >= c.at && t < c.at + 2.6);
	return b ? {text: b.text, age: t - b.at} : null;
};
