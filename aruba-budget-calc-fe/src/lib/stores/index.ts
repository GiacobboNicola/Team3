import { writable, type Writable } from 'svelte/store';
import type { Resource } from '../../types';

export const selectedResources: Writable<Resource[]> = writable([]);

export function addResource(resource: Resource) {
	selectedResources.update((resources) => {
		return [...resources, resource];
	});
}

export function removeResource(resourceId: string) {
	selectedResources.update((resources) => {
		return resources.filter((resource) => resource.id !== resourceId);
	});
}

export function clearResources() {
	selectedResources.set([]);
}
