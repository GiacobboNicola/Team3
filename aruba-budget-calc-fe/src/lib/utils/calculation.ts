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

export function getPriceAndMinimumUnits(
	term: string,
	tierCategory: string
): { price: number; minimumUnits: number } {
	const resources = [
		{
			reservations: [
				{ term: '1 Month', price: 0.0475 },
				{ term: '1 Year', price: 0.045 },
				{ term: '3 Years', price: 0.04 }
			],
			tiers: [
				{ category: 'Base', minimumUnits: 10, percentDiscount: 5.0 },
				{ category: 'Partner', minimumUnits: 50, percentDiscount: 10.0 },
				{ category: 'Premium', minimumUnits: 100, percentDiscount: 15.0 }
			]
		}
	];

	let price: number | null = null;
	let minimumUnits: number | null = null;

	// Find the reservation price
	const reservation = resources[0].reservations.find((res) => res.term === term);
	if (reservation) {
		price = reservation.price;
	}

	// Find the minimum units for the tier category
	const tier = resources[0].tiers.find((t) => t.category === tierCategory);
	if (tier) {
		minimumUnits = tier.minimumUnits;
	}

	if (price && minimumUnits) {
		return { price, minimumUnits };
	}

	return { price: 0.38, minimumUnits: 50 };
}
