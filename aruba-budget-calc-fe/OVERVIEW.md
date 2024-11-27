# Aruba Budget Calculator Overview

The `aruba-budget-calc-fe` is a front-end prototype developed with Svelte 5 and SvelteKit. It is designed to assist Aruba's customers in calculating budgets for their cloud based projects by configuring resources such as containers, cloud computing, storage, and networking, while also providing detailed pricing information.

Ideally, in a more advanced stage, the application will enable users to seamlessly transition from configuration and budgeting to placing an actual order, streamlining the process from planning to procurement.

### Directory Structure

- **src/**
  - **lib/**
    - **components/**: Contains reusable Svelte components such as buttons, forms, and resource selectors.
    - **stores/**: Contains Svelte stores for managing application state, including user and project names, cart items, and resource creation states.
    - **utils/**: Contains utility functions for calculations and data processing.
  - **routes/**: Contains Svelte pages and layouts for different application views.
  - **catalogs/**: Contains JSON files with predefined resource data and pricing information.
  - **types.ts**: Defines TypeScript types and enums used throughout the application.

### Application Flow

1. **User Authentication**: Users start at the main page where they can sign in.
   The login is currently fake, in the future it will be handled via API call and will provide essential information such as the user's Tier and the Token needed to make orders.
2. **Project Creation**: This step is necessary to associate the purchased resources to a project, in the future a project previously created by the user can be selected
3. **Resource Selection**: Users can select a resource type and proceed to configure it.
4. **Configuration**: Users configure the selected resource by specifying technical options (available only for computing units and containers), quantity and reservation details.
5. **Cart Management**: Users can view their cart, which displays selected resources and selected options. They can add new resources or proceed to checkout.
6. **Pricing Calculation**: The application calculates and displays pricing based on user selections and configurations.

### Data Flow

- **State Management**: The application uses Svelte stores to manage state across components. For example, the `resourceCreation` store holds the current step and selected resource, while the `cart` store manages items added to the cart.
- **Derived Stores**: The application uses derived stores to compute values based on other stores, such as total costs based on cart items.
- **Event Handling**: Components handle user interactions through event handlers, updating the state in stores as necessary.

### Real-Time Pricing and Configuration: From Prototype to Product

The use of static files to manage this prototype is a necessary interim solution to ensure the core functionality operates effectively for demonstration purposes. In a future phase of product development, the entire workflow will be integrated through API calls to dedicated backend services. These services will enable dynamic resource configuration, such as determining which RAM options are compatible with a selected CPU, preventing invalid combinations, and calculating applicable discount percentages based on the user’s configuration and Tier (determined at login).

Once the frontend and backend microservices communicate as designed in the architecture, resource pricing will be dynamically calculated in real time based on the selected configuration. During the configuration process, users will be able to see prices update instantly as they adjust their choices.

The purpose of this calculator is to guide users through the process of designing their desired cloud infrastructure, offering an interactive experience that prioritizes intuitiveness and ease of use. Once the configuration of the project's resources is complete, users will have the option to finalize their purchase. This functionality can be fully implemented when the FE communicates seamlessly with the BE, ensuring that price calculations are accurate and reflect all relevant variables.
