import voices from './voices.json';

export const FPS = 30;
export const W = 1920;
export const H = 1080;
export const f = (sec: number) => Math.round(sec * FPS);

// Scene boundaries in seconds.
export const SCENES = {
	cold: [0, 9],
	space: [9, 19.6],
	lobby: [19.6, 45.6],
	machine: [45.6, 63.6],
	rich: [63.6, 74.0],
	broke: [74.0, 79],
	end: [79, 93],
} as const;

export const TOTAL = f(SCENES.end[1]);

export type VoiceId = keyof typeof voices;
export type Speaker = 'narr' | 'req' | 'kli' | 'machine' | 'pigeon' | 'crowd' | 'sfx';

export const speakerOf = (id: VoiceId): Speaker =>
	(({n: 'narr', r: 'req', k: 'kli', v: 'machine', p: 'pigeon', c: 'crowd', s: 'sfx'}) as Record<string, Speaker>)[id[0]] ?? 'sfx';

export const SPEAKER_TAG: Record<Speaker, [string, string] | null> = {
	narr: null,
	sfx: null,
	crowd: ['Everyone', '#ffb3b3'],
	req: ['REQ', '#ff5b5b'],
	kli: ['lojjkli', '#b9b9ff'],
	machine: ['LUCKY SPIN', '#ff5bd6'],
	pigeon: ['THE PIGEON', '#a9b4c4'],
};

export const RESPAWN = 19.6;
export const SPIN1 = 46.2;
export const WIN_PIGEON = 49.0;
export const PECK = 57.6;
export const JACKPOT = 58.4;
export const POOF = 73.4;
export const SPIN2 = 74.2;

export const VOICE_CUES: {id: VoiceId; at: number; vol?: number}[] = [
	{id: 'n_prev', at: 0.6},
	{id: 'n_space', at: 9.6},
	{id: 'r_floor', at: 15.6},
	{id: 'n_lobby', at: 19.8},
	{id: 'k_broke', at: 23.0},
	{id: 'r_prerich', at: 26.6},
	{id: 'r_quit', at: 28.8},
	{id: 'n_day', at: 31.6},
	{id: 'n_min', at: 34.2},
	{id: 'v_req', at: 36.0},
	{id: 'r_changed', at: 38.8},
	{id: 'v_free', at: 40.8},
	{id: 'r_free', at: 42.6},
	{id: 'k_no', at: 43.6},
	{id: 'n_won', at: 49.2},
	{id: 'p_coo', at: 51.6},
	{id: 'r_what', at: 53.4},
	{id: 'n_peck', at: 55.0},
	{id: 'c_jackpot', at: 58.6, vol: 0.9},
	{id: 'r_99', at: 60.0},
	{id: 'n_rich', at: 63.8},
	{id: 'r_gold', at: 68.4},
	{id: 'n_spent', at: 71.0},
	{id: 'v_thanks', at: 76.0},
	{id: 'r_worth', at: 77.7},
	{id: 'n_soon', at: 80.6},
	{id: 'k_earth', at: 86.4},
	{id: 'r_hehe', at: 90.4},
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
	{id: 'riser', at: 3.2, vol: 0.35},
	{id: 'vineboom', at: 4.4, vol: 0.7},
	// space
	{id: 'rumble', at: 9.2, vol: 0.4},
	{id: 'whoosh', at: 17.6, vol: 0.5},
	{id: 'join', at: RESPAWN, vol: 0.5},
	// lobby
	{id: 'lose', at: 23.4, vol: 0.4},
	{id: 'choir', at: 28.8, vol: 0.3},
	{id: 'bells', at: 31.6, vol: 0.3},
	{id: 'scratch', at: 34.0, vol: 0.4},
	{id: 'heartbeat', at: 35.6, vol: 0.4},
	{id: 'sparkle', at: 36.0, vol: 0.5},
	{id: 'sparkle', at: 40.8, vol: 0.6},
	{id: 'whoosh', at: 43.4, vol: 0.6},
	{id: 'chat', at: 44.0, vol: 0.3},
	// machine
	{id: 'tap', at: SPIN1 - 0.2, vol: 0.5},
	{id: 'reel', at: SPIN1, vol: 0.5},
	{id: 'reel', at: SPIN1 + 1.8, vol: 0.5},
	{id: 'pop', at: WIN_PIGEON, vol: 0.6},
	{id: 'vineboom', at: WIN_PIGEON + 0.2, vol: 0.6},
	{id: 'tap', at: PECK, vol: 0.9},
	{id: 'win', at: JACKPOT, vol: 0.7},
	{id: 'bells', at: JACKPOT, vol: 0.5},
	{id: 'diamond', at: JACKPOT + 0.3, vol: 0.5},
	{id: 'cheer', at: JACKPOT + 0.2, vol: 0.5},
	{id: 'chat', at: 60.4, vol: 0.3},
	// rich
	{id: 'purchase', at: 63.8, vol: 0.5},
	{id: 'purchase', at: 66.2, vol: 0.5},
	{id: 'sparkle', at: 68.4, vol: 0.4},
	{id: 'tap', at: 72.8, vol: 0.5},
	{id: 'pop', at: POOF, vol: 0.8},
	{id: 'lose', at: POOF + 0.2, vol: 0.5},
	// broke
	{id: 'reel', at: SPIN2 - 0.4, vol: 0.5},
	{id: 'buzz', at: 75.9, vol: 0.5},
	{id: 'chat', at: 76.4, vol: 0.3},
	// end
	{id: 'braam', at: 79.2, vol: 0.6},
	{id: 'rumble', at: 85.4, vol: 0.5},
	{id: 'vineboom', at: 90.4, vol: 0.7},
];

export const MUSIC_CUES: {id: string; from: number; to: number; vol: number; fadeIn?: number; fadeOut?: number; offset?: number}[] = [
	{id: 'intro', from: 0, to: 9.2, vol: 0.5, fadeOut: 0.8},
	{id: 'mystery', from: 9.2, to: 19.4, vol: 0.28, fadeIn: 0.5, fadeOut: 0.3},
	{id: 'lobby', from: 19.6, to: 34.0, vol: 0.28, fadeIn: 0.4, fadeOut: 0.05},
	{id: 'mystery', from: 35.4, to: 45.4, vol: 0.32, fadeIn: 0.6, fadeOut: 0.3},
	{id: 'chaos', from: 45.6, to: 58.3, vol: 0.3, fadeIn: 0.1, fadeOut: 0.1},
	{id: 'party', from: JACKPOT, to: POOF, vol: 0.32, fadeIn: 0.05, fadeOut: 0.05, offset: 4},
	{id: 'sad', from: POOF + 0.6, to: 78.8, vol: 0.3, fadeIn: 0.3, fadeOut: 0.5},
	{id: 'intro', from: 79.0, to: 84.8, vol: 0.45, fadeIn: 0.2, fadeOut: 1.0, offset: 3},
	{id: 'mystery', from: 85.2, to: 93, vol: 0.26, fadeIn: 0.5, fadeOut: 0.6, offset: 3},
];

export type ChatLine = {at: number; name: string; text: string; color?: string; system?: boolean};

export const CHAT: ChatLine[] = [
	{at: 44.0, name: 'GamingSquirrel39', text: 'bro lasted 3 minutes 💀', color: '#ffd166'},
	{at: 60.4, name: 'kaiib', text: 'THE PIGEON IS GOATED', color: '#9cff8a'},
	{at: 76.4, name: 'lewlone', text: 'he really did it again', color: '#7ad1ff'},
];

export const bubbleOf = (name: string, t: number) => {
	const b = [...CHAT].reverse().find((c) => c.name === name && t >= c.at && t < c.at + 2.6);
	return b ? {text: b.text, age: t - b.at} : null;
};
