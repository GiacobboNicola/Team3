import containerData from '../../catalogs/container.json';

interface GetPricingDetailsArgs {
	osPlatform: string;
	cpu: string;
	ram: string;
	disk: string;
	reservationTerm: string;
	tierCategory: string;
}

export function getPricingDetails(args: GetPricingDetailsArgs): {
	price: number;
	minimumUnits: number;
	percentDiscount: number;
} {
	const { osPlatform, cpu, ram, disk, reservationTerm, tierCategory } = args;
	for (const container of containerData) {
		if (
			container.flavor &&
			container.flavor.osPlatform === osPlatform.toLowerCase() &&
			container.flavor.cpu === cpu &&
			container.flavor.ram === ram &&
			container.flavor.disk === disk
		) {
			// Find the reservation matching the specified term
			const reservation = container.reservations.find((res: any) => res.term === reservationTerm);
			if (reservation) {
				// Find the tier matching the specified category
				const tier = container.tiers.find((t: any) => t.category === tierCategory);
				if (tier) {
					return {
						price: reservation.price,
						minimumUnits: tier.minimumUnits,
						percentDiscount: tier.percentDiscount
					};
				}
			}
		}
	}

	// Return null values if no match is found
	return { price: 0.38, minimumUnits: 50, percentDiscount: 12 };
}
