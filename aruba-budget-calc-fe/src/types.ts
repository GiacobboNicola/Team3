export interface PricingOption {
	name: string;
	discount: number;
	minUnits: number;
}

export interface ServerOptions {
	os: string[];
	cpu: string[];
	ram: string[];
	disk: string[];
}

export enum ResourceName {
	DISK = 'disk',
	NETWORKING = 'networking',
	CONTAINER = 'container',
	COMPUTING = 'computing'
}

export enum StepName {
	RESOURCETYPESELECTOR,
	SERVERCONFIGURATOR,
	PROJECTNAMEFORM,
	QUANTITYRESERVATIONFORM
}

export interface Resource {
	id: string;
	name: ResourceName;
	hourlyPrice?: number;
	flavorId?: string;
	os?: string[] | undefined;
	reservationPrice?: {
		month: {
			base: number;
			partner: number;
			premium: number;
		};
		year: {
			base: number;
			partner: number;
			premium: number;
		};
		threeYears: {
			base: number;
			partner: number;
			premium: number;
		};
	};
	minimumUnits?: {
		base: number;
		partner: number;
		premium: number;
	};
}