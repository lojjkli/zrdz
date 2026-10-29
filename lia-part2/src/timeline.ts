import voices from './voices.json';

export const FPS = 30;
export const W = 1920;
export const H = 1080;
export const f = (sec: number) => Math.round(sec * FPS);

// Scene boundaries in seconds.
export const SCENES = {
	cold: [0, 10],
	home: [10, 29],
	lobby: [29, 40.2],
	casino: [40.2, 58.5],
	party: [58.5, 92],
	end: [92, 105],
} as const;

export const TOTAL = f(SCENES.end[1]);

export type VoiceId = keyof typeof voices;
export type Speaker = 'narr' | 'lia' | 'boomp' | 'kids' | 'mikey' | 'ade' | 'req' | 'kid' | 'kli' | 'donut' | 'pigeon' | 'sfx';

export const speakerOf = (id: VoiceId): Speaker =>
	(({n: 'narr', l: 'lia', b: 'boomp', c: 'kids', m: 'mikey', a: 'ade', r: 'req', x: 'kid', k: 'kli', d: 'donut', p: 'pigeon', s: 'sfx'}) as Record<string, Speaker>)[id[0]] ?? 'sfx';

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
};

export const SPIN = 43.0;
export const JACKPOT = 50.6;
export const FART = 78.6;
export const FALL = 85.0;

export const VOICE_CUES: {id: VoiceId; at: number; vol?: number}[] = [
	{id: 'n_prev', at: 0.8},
	{id: 'n_respawn', at: 7.2},
	{id: 'n_moved', at: 10.6},
	{id: 'b_dinner', at: 16.2},
	{id: 'c_67', at: 18.0, vol: 0.9},
	{id: 'l_count', at: 20.0},
	{id: 'l_missing', at: 24.0},
	{id: 'l_help', at: 26.4},
	{id: 'm_bro', at: 29.8},
	{id: 'a_track', at: 32.4},
	{id: 'n_tracks', at: 35.0},
	{id: 'n_found', at: 38.0},
	{id: 'r_natural', at: 41.0},
	{id: 'x_spin', at: 42.8},
	{id: 'l_req', at: 44.6},
	{id: 'r_99', at: 45.8},
	{id: 'n_jackpot', at: 49.0},
	{id: 'c_what', at: 51.6, vol: 0.9},
	{id: 'x_keep', at: 53.6},
	{id: 'l_fine', at: 56.4},
	{id: 'n_party', at: 59.0},
	{id: 'k_wsg', at: 63.4},
	{id: 'd_hello', at: 68.0},
	{id: 'c_donut', at: 70.0, vol: 0.9},
	{id: 'r_feel', at: 73.0},
	{id: 'c_no', at: 75.0, vol: 0.9},
	{id: 'l_dont', at: 76.0},
	{id: 'n_tiny', at: 80.0},
	{id: 'r_hehe', at: 83.6},
	{id: 'n_windmill', at: 88.0},
	{id: 'n_soon', at: 93.8},
	{id: 'l_68', at: 99.6},
	{id: 'p_coo', at: 102.6},
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
	{id: 'riser', at: 3.6, vol: 0.35},
	{id: 'vineboom', at: 4.9, vol: 0.7},
	{id: 'join', at: 7.4, vol: 0.4},
	// home
	{id: 'bells', at: 16.0, vol: 0.3},
	{id: 'cheer', at: 18.0, vol: 0.35},
	{id: 'pop', at: 21.5, vol: 0.4},
	{id: 'pop', at: 22.3, vol: 0.4},
	{id: 'pop', at: 23.1, vol: 0.4},
	{id: 'vineboom', at: 24.0, vol: 0.8},
	{id: 'siren', at: 26.4, vol: 0.25, dur: 2.2},
	{id: 'chat', at: 27.2, vol: 0.3},
	// lobby
	{id: 'sparkle', at: 35.2, vol: 0.4},
	{id: 'steps', at: 35.8, vol: 0.4},
	{id: 'riser', at: 38.4, vol: 0.4},
	// casino
	{id: 'vineboom', at: 40.2, vol: 0.9},
	{id: 'tap', at: SPIN - 0.2, vol: 0.5},
	...[0, 1, 2, 3].map((i) => ({id: 'reel' as Sfx, at: SPIN + i * 1.8, vol: 0.5})),
	{id: 'chat', at: 46.6, vol: 0.3},
	{id: 'pop', at: 49.4, vol: 0.5},
	{id: 'pop', at: 49.9, vol: 0.5},
	{id: 'win', at: JACKPOT, vol: 0.7},
	{id: 'bells', at: JACKPOT, vol: 0.5},
	{id: 'purchase', at: JACKPOT + 0.4, vol: 0.5},
	{id: 'sparkle', at: 51.0, vol: 0.5},
	{id: 'chat', at: 52.2, vol: 0.3},
	{id: 'heartpop', at: 54.0, vol: 0.4},
	{id: 'scratch', at: 56.3, vol: 0.3},
	// party
	{id: 'whoosh', at: 61.6, vol: 0.6},
	{id: 'land', at: 63.0, vol: 0.7},
	{id: 'whoosh', at: 66.2, vol: 0.4},
	{id: 'cheer', at: 70.0, vol: 0.5},
	{id: 'scratch', at: 72.6, vol: 0.7},
	{id: 'vineboom', at: 74.5, vol: 0.6},
	{id: 'chat', at: 75.4, vol: 0.3},
	{id: 'heartbeat', at: 77.0, vol: 0.5},
	{id: 'tinyfart', at: FART, vol: 0.8},
	{id: 'chat', at: 84.6, vol: 0.3},
	{id: 'crack', at: FALL - 0.3, vol: 0.5},
	{id: 'rumble', at: FALL + 0.4, vol: 0.5},
	{id: 'bigboom', at: FALL + 2.0, vol: 0.7},
	{id: 'chat', at: 89.8, vol: 0.3},
	// end
	{id: 'braam', at: 92.2, vol: 0.6},
	{id: 'scratch', at: 101.6, vol: 0.4},
	{id: 'vineboom', at: 102.6, vol: 0.8},
];

export const MUSIC_CUES: {id: string; from: number; to: number; vol: number; fadeIn?: number; fadeOut?: number; offset?: number}[] = [
	{id: 'intro', from: 0, to: 10.2, vol: 0.5, fadeOut: 0.8},
	{id: 'romance', from: 10.2, to: 23.8, vol: 0.26, fadeIn: 0.8, fadeOut: 0.3, offset: 2},
	{id: 'mystery', from: 24.2, to: 40.0, vol: 0.3, fadeIn: 0.5, fadeOut: 0.2},
	{id: 'chaos', from: 40.2, to: 50.5, vol: 0.3, fadeIn: 0.05, fadeOut: 0.1},
	{id: 'party', from: JACKPOT, to: 58.3, vol: 0.3, fadeIn: 0.05, fadeOut: 0.5, offset: 4},
	{id: 'party', from: 58.5, to: 72.6, vol: 0.32, fadeIn: 0.6, fadeOut: 0.05},
	{id: 'sad', from: FALL + 2.2, to: 91.8, vol: 0.3, fadeIn: 0.3, fadeOut: 0.6},
	{id: 'intro', from: 92.0, to: 97.6, vol: 0.45, fadeIn: 0.2, fadeOut: 1.0, offset: 3},
	{id: 'mystery', from: 98.2, to: 105, vol: 0.26, fadeIn: 0.5, fadeOut: 0.6, offset: 3},
];

export type ChatLine = {at: number; name: string; text: string; color?: string; system?: boolean};

export const CHAT: ChatLine[] = [
	{at: 27.2, name: 'Emii5287', text: 'how do u lose a kid 😭', color: '#ff9ad5'},
	{at: 46.6, name: 'pet_trader99', text: 'REQ is teaching a kid to gamble 💀', color: '#ffd166'},
	{at: 52.2, name: 'kaiib', text: 'GOLDEN DRAGON??', color: '#9cff8a'},
	{at: 75.4, name: 'Toast_YT', text: 'EVERYBODY RUN', color: '#ffd166'},
	{at: 84.6, name: 'Emii5287', text: 'that was it? 😭', color: '#ff9ad5'},
	{at: 89.8, name: 'HachiMC', text: 'rip windmill 🕊️', color: '#7ad1ff'},
];

export const bubbleOf = (name: string, t: number) => {
	const b = [...CHAT].reverse().find((c) => c.name === name && t >= c.at && t < c.at + 2.6);
	return b ? {text: b.text, age: t - b.at} : null;
};
