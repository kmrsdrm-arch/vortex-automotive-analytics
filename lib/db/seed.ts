import { db, vehicles, sales, inventory } from "./index";
import { faker } from "@faker-js/faker";

const VEHICLE_CATEGORIES = ["Sedan", "SUV", "Truck", "Coupe", "Convertible", "Minivan"];
const REGIONS = ["North", "South", "East", "West", "Central"];
const CUSTOMER_SEGMENTS = ["Individual", "Fleet", "Corporate"];
const MAKES = ["Toyota", "Honda", "Ford", "Chevrolet", "BMW", "Mercedes", "Audi", "Tesla"];

async function seed() {
  console.log("🌱 Starting database seeding...");

  try {
    // Create vehicles
    console.log("Creating vehicles...");
    const vehicleIds: number[] = [];
    
    for (let i = 0; i < 100; i++) {
      const make = faker.helpers.arrayElement(MAKES);
      const category = faker.helpers.arrayElement(VEHICLE_CATEGORIES);
      
      const [vehicle] = await db.insert(vehicles).values({
        vin: faker.vehicle.vin(),
        make,
        model: faker.vehicle.model(),
        year: faker.number.int({ min: 2020, max: 2024 }),
        category,
        msrp: faker.number.int({ min: 25000, max: 85000 }).toString(),
        specifications: {
          color: faker.vehicle.color(),
          fuelType: faker.vehicle.fuel(),
          transmission: faker.helpers.arrayElement(["Automatic", "Manual"]),
        },
      }).returning({ id: vehicles.id });
      
      vehicleIds.push(vehicle.id);
    }
    console.log(`✓ Created ${vehicleIds.length} vehicles`);

    // Create sales records (last 6 months)
    console.log("Creating sales records...");
    const salesCount = 5000;
    
    for (let i = 0; i < salesCount; i++) {
      const vehicleId = faker.helpers.arrayElement(vehicleIds);
      const quantity = faker.number.int({ min: 1, max: 3 });
      const basePrice = faker.number.int({ min: 25000, max: 85000 });
      const totalAmount = (basePrice * quantity).toString();
      
      // Generate sale date within last 180 days
      const daysAgo = faker.number.int({ min: 0, max: 180 });
      const saleDate = new Date();
      saleDate.setDate(saleDate.getDate() - daysAgo);

      await db.insert(sales).values({
        vehicleId,
        saleDate,
        quantity,
        totalAmount,
        customerSegment: faker.helpers.arrayElement(CUSTOMER_SEGMENTS),
        region: faker.helpers.arrayElement(REGIONS),
        dealerName: `${faker.company.name()} Auto`,
      });
    }
    console.log(`✓ Created ${salesCount} sales records`);

    // Create inventory records
    console.log("Creating inventory records...");
    
    for (const vehicleId of vehicleIds) {
      const region = faker.helpers.arrayElement(REGIONS);
      const quantityAvailable = faker.number.int({ min: 0, max: 50 });
      
      let status = "in_stock";
      if (quantityAvailable === 0) status = "out_of_stock";
      else if (quantityAvailable < 10) status = "low_stock";

      await db.insert(inventory).values({
        vehicleId,
        warehouse: `${region} Distribution Center`,
        region,
        quantityAvailable,
        status,
        lastUpdated: new Date(),
      });
    }
    console.log(`✓ Created ${vehicleIds.length} inventory records`);

    console.log("✅ Database seeding completed successfully!");
  } catch (error) {
    console.error("❌ Error seeding database:", error);
    throw error;
  }
}

seed()
  .catch((error) => {
    console.error("Seed failed:", error);
    process.exit(1);
  });

