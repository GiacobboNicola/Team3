import { writable } from 'svelte/store';
import type { ResourceName, ServerOptions } from '../../types';

interface CartItem {
	id: string;
	resourceType: ResourceName;
	serverConfig?: Record<keyof ServerOptions, string | null>;
	quantity: number;
	period: string;
}

export const cart = writable<CartItem[]>([]);

export const cartActions = {
	addItem: (item: Omit<CartItem, 'id'>) => {
		cart.update((items) => [...items, { ...item, id: crypto.randomUUID() }]);
	},

	removeItem: (id: string) => {
		cart.update((items) => items.filter((item) => item.id !== id));
	},

	clearCart: () => {
		cart.set([]);
	}
};
