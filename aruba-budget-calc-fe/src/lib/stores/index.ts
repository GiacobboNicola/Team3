import { writable, type Writable } from 'svelte/store';

export const projectName: Writable<string> = writable('');
export const userName: Writable<string> = writable('');

export function setProjectName(name: string) {
	projectName.set(name);
}

export function setUserName(name: string) {
	userName.set(name);
}
