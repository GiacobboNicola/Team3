import { writable } from 'svelte/store';
import { StepName, type ResourceName, type ServerOptions } from '../../types';

interface ResourceCreationState {
	currentStep: number;
	selectedResource?: ResourceName;
	serverConfig?: Record<keyof ServerOptions, string | null>;
	quantity?: number;
	period?: string;
}

const initialState: ResourceCreationState = {
	currentStep: StepName.INITIALGRID,
	selectedResource: undefined,
	serverConfig: undefined,
	quantity: undefined,
	period: undefined
};

export const resourceCreation = writable<ResourceCreationState>(initialState);

// Actions
export const resourceCreationActions = {
	reset: () => {
		resourceCreation.set(initialState);
	},

	setStep: (step: number) => {
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
			quantity: quantity
		}));
	},

	setPeriod: (period: string) => {
		resourceCreation.update((state) => ({
			...state,
			period: period
		}));
	}
};
