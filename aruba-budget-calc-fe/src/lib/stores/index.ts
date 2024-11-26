import { writable, type Writable } from 'svelte/store';

export const projectName: Writable<string> = writable('');

export function setProjectName(name: string) {
	projectName.set(name);
}
