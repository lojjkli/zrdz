// Script format shared by all story projects. Times are worked out in timeline.ts from the voice lengths.

/** [sfx id, seconds after the line starts (can be negative), volume, max duration] */
export type SfxCue = [string, number, number?, number?];

type Extras = {
	mark?: string;
	sfx?: SfxCue[];
	/** big pop-up text: text, or [text, color, size] */
	big?: string | [string, string?, number?];
	flash?: boolean | string;
	chat?: [string, string];
	/** camera: 'wide', 'wide2', an actor id (close-up), 'two:a,b', or a named shot of the scene */
	shot?: string;
	shake?: number;
};

export type Beat =
	| ({card: 'title' | 'tbc' | 'end'; dur: number; text?: string; sub?: string; color?: string; music?: string} & Extras)
	| {scene: string; music?: string; vol?: number; offset?: number}
	| ({wait: number} & Extras)
	| ({id: string; gap?: number; hold?: number; vol?: number} & Extras);
