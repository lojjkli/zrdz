import voices from './voices.json';
import {Beat, SCRIPT, SPEAKERS} from './script';

export const FPS = 30;
export const W = 1920;
export const H = 1080;
export const f = (sec: number) => Math.round(sec * FPS);

type VoiceMeta = {sec: number; text: string; file: string};
const V = voices as Record<string, VoiceMeta>;

export type VoiceId = string;
export type Speaker = string;

// voice ids look like "req_hello"; "n_..." is the narrator
export const speakerOf = (id: VoiceId): Speaker => {
	const s = id.split('_')[0];
	return s === 'n' ? 'narr' : s;
};

export const SPEAKER_TAG: Record<Speaker, [string, string] | null> = {narr: null, sfx: null, ...SPEAKERS};

export const voiceSec = (id: VoiceId) => V[id]?.sec ?? 1.5;
export const voiceText = (id: VoiceId) => V[id]?.text ?? id;
export const voiceFile = (id: VoiceId) => V[id]?.file ?? '';

export type Sfx = string;
export type CardKind = 'title' | 'tbc' | 'end';

export type Span = {key: string; from: number; to: number; card?: CardKind; text?: string; sub?: string; color?: string; scene?: string};
export type BeatWin = {from: number; to: number; at: number; id?: string; speaker?: Speaker; shot?: string; shake?: number; scene: string; n: number};

export const SPANS: Span[] = [];
export const BEATS: BeatWin[] = [];
/** start time of each voice line */
export const T: Record<string, number> = {};
/** named moments */
export const M: Record<string, number> = {};
export const VOICE_CUES: {id: VoiceId; at: number; vol?: number}[] = [];
export const SFX_CUES: {id: Sfx; at: number; vol?: number; dur?: number}[] = [];
export const MUSIC_CUES: {id: string; from: number; to: number; vol: number; fadeIn?: number; fadeOut?: number; offset?: number}[] = [];
export const BIGS: {from: number; to: number; text: string; color?: string; size?: number; top?: number}[] = [];
export const FLASHES: {at: number; color?: string}[] = [];

export type ChatLine = {at: number; name: string; text: string; color?: string; system?: boolean};
export const CHAT: ChatLine[] = [];
export const TAPS: [number, number, number][] = [];

const CHAT_COLORS = ['#ffd166', '#9cff8a', '#7ad1ff', '#ff9ad5', '#ffb36b'];

(() => {
	let c = 0;
	let cur: Span | null = null;
	let music: {id: string; vol: number; offset?: number} | null = null;
	let n = 0;
	const close = () => {
		if (cur) {
			cur.to = c;
			SPANS.push(cur);
			if (music) MUSIC_CUES.push({id: music.id, from: cur.from, to: c, vol: music.vol, fadeIn: 0.3, fadeOut: 0.4, offset: music.offset});
		}
		cur = null;
	};
	const extras = (b: Beat, at: number, to: number) => {
		if ('mark' in b && b.mark) M[b.mark] = at;
		if ('sfx' in b && b.sfx) for (const [id, dt, vol, dur] of b.sfx) SFX_CUES.push({id, at: at + dt, vol: vol ?? 0.6, dur});
		if ('big' in b && b.big) {
			const [text, color, size] = typeof b.big === 'string' ? [b.big] : b.big;
			BIGS.push({from: at, to: Math.max(at + 1.6, Math.min(to, at + 2.6)), text, color, size});
		}
		if ('flash' in b && b.flash) FLASHES.push({at, color: b.flash === true ? '#fff' : b.flash});
		if ('chat' in b && b.chat) CHAT.push({at, name: b.chat[0], text: b.chat[1], color: CHAT_COLORS[CHAT.length % CHAT_COLORS.length]});
	};
	for (const b of SCRIPT) {
		if ('card' in b) {
			close();
			music = null;
			cur = {key: 'card' + SPANS.length, from: c, to: 0, card: b.card, text: b.text, sub: b.sub, color: b.color};
			if (b.music) MUSIC_CUES.push({id: b.music, from: c, to: c + b.dur, vol: 0.5, fadeIn: 0.05, fadeOut: 0.8});
			extras(b, c, c + b.dur);
			c += b.dur;
			close();
		} else if ('scene' in b) {
			close();
			cur = {key: b.scene + SPANS.length, from: c, to: 0, scene: b.scene};
			music = b.music ? {id: b.music, vol: b.vol ?? 0.28, offset: b.offset} : null;
		} else if ('wait' in b) {
			const scene = (cur as Span | null)?.scene ?? '';
			BEATS.push({from: c, to: c + b.wait, at: c, shot: b.shot, shake: b.shake, scene, n: n++});
			extras(b, c, c + b.wait);
			c += b.wait;
		} else {
			const scene = (cur as Span | null)?.scene ?? '';
			const at = c + (b.gap ?? 0.35);
			const end = at + voiceSec(b.id);
			T[b.id] = at;
			VOICE_CUES.push({id: b.id, at, vol: b.vol});
			BEATS.push({from: c, to: end + (b.hold ?? 0), at, id: b.id, speaker: speakerOf(b.id), shot: b.shot, shake: b.shake, scene, n: n++});
			extras(b, at, end + (b.hold ?? 0));
			c = end + (b.hold ?? 0);
		}
	}
	close();
	// the freeze frame keeps the previous scene's name
	SPANS.forEach((s, i) => {
		if (s.card === 'tbc' && i > 0) s.scene = SPANS[i - 1].scene;
	});
})();

export const TOTAL = f(SPANS[SPANS.length - 1].to);

export const talking = (who: Speaker, t: number) =>
	VOICE_CUES.some((c) => speakerOf(c.id) === who && t >= c.at && t <= c.at + voiceSec(c.id) - 0.05);

export const beatAt = (t: number) => BEATS.find((b) => t >= b.from && t < b.to) ?? null;

export const bubbleOf = (name: string, t: number) => {
	const b = [...CHAT].reverse().find((c) => c.name === name && t >= c.at && t < c.at + 2.6);
	return b ? {text: b.text, age: t - b.at} : null;
};
