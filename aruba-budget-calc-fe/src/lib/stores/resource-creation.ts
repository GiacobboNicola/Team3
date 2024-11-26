import { writable } from 'svelte/store';
import type { ResourceName, ServerOptions } from '../../types';
import { StepName } from '../../types';

interface ResourceCreationState {
	currentStep: StepName;
	selectedResource?: ResourceName;
	serverConfig?: Record<keyof ServerOptions, string | null>;
	quantity?: number;
	period?: string;
	price?: number;
}

const initialState: ResourceCreationState = {
	currentStep: StepName.RESOURCETYPESELECTOR,
	selectedResource: undefined,
	serverConfig: undefined,
	quantity: undefined,
	period: undefined,
	price: 0
};

export const resourceCreation = writable<ResourceCreationState>(initialState);

// Actions
export const resourceCreationActions = {
	reset: () => {
		resourceCreation.set(initialState);
	},

	setStep: (step: StepName) => {
		resourceCreation.update((state) => ({
			...state,
			currentStep: step
		}));
	},

	setResource: (resource: ResourceName) => {
		resourceCreation.update((state) => ({
			...state,
			selectedResource: resource
		}));
	},

	setServerConfig: (config: Record<keyof ServerOptions, string | null>) => {
		resourceCreation.update((state) => ({
			...state,
			serverConfig: config
		}));
	},

	setQuantity: (quantity: number) => {
		resourceCreation.update((state) => ({
			...state,
			quantity
		}));
	},

	setPeriod: (period: string) => {
		resourceCreation.update((state) => ({
			...state,
			period
		}));
	},

	setPrice: (price: number) => {
		resourceCreation.update((state) => ({
			...state,
			price
		}));
	}
};
