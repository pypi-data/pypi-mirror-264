# Input Change Catalog #

This document attempts to categorize the changes made to the schema so that the changes can be generalized.

## 9.4 to 9.5 ##

### Object Change: Construction:AirBoundary
Removes two fields ("Solar and Daylighting Method" and "Radiant Exchange Method") and warns for values other than "GroupedZones".

## 22.1 to 22.2 ##


## 22.1 to 22.2 ##


## 22.2 to 23.1 ##


## 23.1 to 23.2 ##

### Object Change: Coil:Cooling:DX:CurveFit:Performance
### Object Change: Coil:Cooling:DX:SingleSpeed
### Object Change: Coil:Cooling:DX:MultiSpeed
### Object Change: Coil:Cooling:DX:TwoStageWithHumidityControlMode
### Object Change: Coil:Heating:DX:SingleSpeed
### Object Change: Coil:Heating:DX:MultiSpeed
### Object Change: Coil:Heating:DX:VariableSpeed
### Object Change: Coil:WaterHeating:AirToWaterHeatPump:Pumped
### Object Change: Coil:WaterHeating:AirToWaterHeatPump:Wrapped
### Object Change: Coil:WaterHeating:AirToWaterHeatPump:VariableSpeed

All of these objects add an optional field, no change in the epJSON

### Object Change: Site:GroundTemperature:Undisturbed:Xing
Change the name of the field "Average Soil Surface Tempeature" to "Average Soil Surface Temperature".





### Object Change: Construction:ComplexFenestrationState
Change the name of fields:

    - Fields 11, 17, 23, 29, 35 from "Outside Layer X Directional Front Absoptance Matrix Name" to "Outside Layer X Directional Front Absorptance Matrix Name"
    - Fields 12, 18, 24, 30, 36 from "Outside Layer X Directional Back Absoptance Matrix Name" to "Outside Layer X Directional Back Absorptance Matrix Name"
    - Fields 14, 20, 26, 32 from "Gap X Directional Front Absoptance Matrix Name" to "Gap X Directional Front Absorptance Matrix Name"
    - Fields 15, 21, 27, 33 from "Gap X Directional Back Absoptance Matrix Name" to "Gap X Directional Back Absorptance Matrix Name".

### Object Change: Coil:Heating:Fuel
Change the name of fields from "Parasitic Electric Load {W}" to "On Cycle Parasitic Electric Load {W}" and from "Parasitic Fuel Load {W}" to "Off Cycle Parasitic Fuel Load {W}".

### Object Change: Coil:Heating:Gas:MultiStage
Change the name of fields:

    - "Parasitic Gas Load {W}" to "Off Cycle Parasitic Gas Load {W}"
    - "Stage 1 Parasitic Electric Load {W}" to "Stage 1 On Cycle Parasitic Electric Load {W}"
    - "Stage 2 Parasitic Electric Load {W}" to "Stage 2 On Cycle Parasitic Electric Load {W}"
    - "Stage 3 Parasitic Electric Load {W}" to "Stage 3 On Cycle Parasitic Electric Load {W}"
    - "Stage 4 Parasitic Electric Load {W}" to "Stage 4 On Cycle Parasitic Electric Load {W}".

### Object Change: Coil:Heating:Desuperheater
Change the name of the field "Parasitic Electric Load {W}" to "On Cycle Parasitic Electric Load {W}".

### Object Change: Boiler:HotWater
Change the name of the field "Parasitic Electric Load {W}" to "On Cycle Parasitic Electric Load {W}".

### Object Change: SurfaceProperty:LocalEnvironment
Change the name of the field "External Shading Fraction Schedule Name" to "Sunlit Fraction Schedule Name".

### Object Change: LoadProfile:Plant
Adds optional fields, no change to the epJSON

### Object Change: DistrictHeating to DistrictHeating:Water
Change the object name from DistrictHeating to DistrictHeating:Water.

### Object Change: OtherEquipment
### Object Change: Exterior:FuelEquipment
### Object Change: ZoneHVAC:HybridUnitaryHVAC
### Object Change: WaterHeater:Mixed


### Object Change: WaterHeater:Stratified
Field 20 remains the same. - Choice key Steam has been replaced with DistrictHeatingSteam. - Choice key DistrictHeating has been replaced with DistrictHeatingWater.

See PR#9260

### Object Change: EnergyManagementSystem:MeteredOutputVariable
### Object Change: Meter:Custom
### Object Change: Meter:CustomDecrement
### Object Change: PythonPlugin:OutputVariable
Choice key Steam has been replaced with DistrictHeatingSteam. - Choice key DistrictHeating has been replaced with DistrictHeatingWater.

### Object Change: EnvironmentalImpactFactors
Change field from "District Heating Efficiency" to "District Heating Water Efficiency" and field from "Steam Conversion Efficiency" to "District Heating Steam Conversion Efficiency".

### Object Change: LifeCycleCost:UsePriceEscalation
### Object Change: LifeCycleCost:UseAdjustment
Choice key Steam has been replaced with DistrictHeatingSteam for field "Resource".