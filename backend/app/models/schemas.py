from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    food_name: str = Field(default="Biscuits", description="Name of the food product")
    food_category: str = Field(default="Cereals and cereal products", description="Category of the food")
    
    # Food Characteristics
    moisture_level: float = Field(default=4.5, description="Moisture content in % (e.g. 4.5 for biscuits, 85 for fruit)")
    fat_oil_sensitivity: str = Field(default="Medium", description="Low, Medium, or High sensitivity to lipid oxidation")
    ph: float = Field(default=6.5, description="Product pH (e.g. 3.5 for citrus, 6.5 for biscuits)")
    respiration_activity: str = Field(default="Low", description="Low, Medium, or High (for fresh horticultural produce)")

    # Shelf Life & Storage
    desired_shelf_life_days: int = Field(default=180, description="Target shelf-life in days")
    storage_temperature_c: float = Field(default=25.0, description="Storage temperature in Celsius")
    relative_humidity_pct: float = Field(default=65.0, description="Ambient relative humidity %")
    storage_condition: str = Field(default="Ambient", description="Ambient, Refrigerated, Chilled, or Frozen")
    transport_condition: str = Field(default="Ambient / Road", description="Logistics rigor: Ambient, Rough, Export, Cold-Chain")

    # Packaging Requirements
    map_required: str = Field(default="No", description="Yes, No, or Optional")
    sustainability_priority: str = Field(default="Standard", description="Standard, High (Recyclable), or Strict (Zero-Plastic)")
    preferred_package_type: str = Field(default="Any", description="Any, Flexible, Rigid, Bottle, Pouch, Box, Can")

class ScoringWeightsUpdate(BaseModel):
    barrier_score: float = 0.2857
    compatibility_score: float = 0.2143
    shelf_life_score: float = 0.2143
    mechanical_score: float = 0.1429
    sustainability_score: float = 0.1428
