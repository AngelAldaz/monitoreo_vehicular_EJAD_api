import pandas as pd
from io import BytesIO
from typing import List, Dict, Any
from app.models.routesModel import Route
from app.models.fuelStopsModel import FuelStop
from app.models.vehiclesModel import Vehicle

class ExcelGenerator:
    @staticmethod
    def generate_vehicle_report(vehicle: Vehicle, routes: List[Route], fuel_stops_by_route: Dict[int, List[FuelStop]]) -> BytesIO:
        """
        Generate an Excel report for a vehicle with its routes and fuel stops
        
        Args:
            vehicle: The vehicle to report on
            routes: List of routes for the vehicle
            fuel_stops_by_route: Dictionary mapping route IDs to their fuel stops
            
        Returns:
            BytesIO object containing the Excel file
        """
        output = BytesIO()
        
        # Create Excel writer
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Create vehicle sheet
            vehicle_data = {
                "ID": [vehicle.id_vehicle],
                "Number Plate": [vehicle.number_plate],
                "Serial Number": [vehicle.serial_number],
                "Brand": [vehicle.brand.name if vehicle.brand else ""],
                "Model": [vehicle.model.name if vehicle.model else ""],
                "Description": [vehicle.description.name if vehicle.description else ""],
                "Year": [vehicle.year],
                "Color": [vehicle.color],
                "Current KM": [vehicle.km],
                "KM per Liter": [vehicle.km_per_litre],
                "Current Route Status": [vehicle.route_status.value],
                "Assignment Status": [vehicle.assignment_status.value]
            }
            vehicle_df = pd.DataFrame(vehicle_data)
            vehicle_df.to_excel(writer, sheet_name="Vehicle Info", index=False)
            
            # Create routes sheet
            if routes:
                routes_data = []
                for route in routes:
                    # Safely get distance using the hybrid property
                    distance = route.total_km if hasattr(route, 'total_km') else 0
                    if distance == 0 and hasattr(route, 'end_km') and hasattr(route, 'start_km') and route.end_km and route.start_km:
                        distance = route.end_km - route.start_km
                    
                    # Safely get user full name
                    driver_name = ""
                    if hasattr(route, 'user') and route.user:
                        driver_name = f"{route.user.first_name} {route.user.last_name}" if hasattr(route.user, 'first_name') else ""
                    
                    route_data = {
                        "ID": route.id_route,
                        "Description": route.description if hasattr(route, 'description') else "",
                        "Driver": driver_name,
                        "Start Time": route.start_time if hasattr(route, 'start_time') else None,
                        "End Time": route.end_time if hasattr(route, 'end_time') else None,
                        "Start KM": route.start_km if hasattr(route, 'start_km') else 0,
                        "End KM": route.end_km if hasattr(route, 'end_km') else 0,
                        "Distance (KM)": distance,
                        "Duration (hours)": route.total_duration if hasattr(route, 'total_duration') and route.total_duration else 0,
                        "Estimated KM": route.estimated_km if hasattr(route, 'estimated_km') and route.estimated_km else 0,
                        "Estimated Time": route.estimated_time if hasattr(route, 'estimated_time') and route.estimated_time else 0,
                        "On Time": "Yes" if hasattr(route, 'on_time') and route.on_time else "No",
                        "On Distance": "Yes" if hasattr(route, 'on_distance') and route.on_distance else "No",
                        "Liters Consumed": route.liters_consumed if hasattr(route, 'liters_consumed') and route.liters_consumed else 0
                    }
                    routes_data.append(route_data)
                
                routes_df = pd.DataFrame(routes_data)
                routes_df.to_excel(writer, sheet_name="Routes", index=False)
            
            # Create fuel stops sheet for each route with fuel stops
            for route_id, fuel_stops in fuel_stops_by_route.items():
                if fuel_stops:
                    route = next((r for r in routes if r.id_route == route_id), None)
                    if route:
                        sheet_name = f"Route {route_id} Fuel Stops"
                        if len(sheet_name) > 31:  # Excel has 31 char limit for sheet names
                            sheet_name = sheet_name[:31]
                            
                        fuel_stops_data = []
                        for stop in fuel_stops:
                            # Safely calculate stop duration
                            stop_duration = 0
                            if hasattr(stop, 'resume_time') and hasattr(stop, 'stop_time') and stop.resume_time and stop.stop_time:
                                stop_duration = round((stop.resume_time - stop.stop_time).total_seconds() / 60)
                            
                            stop_data = {
                                "ID": stop.id_fuel_stop if hasattr(stop, 'id_fuel_stop') else 0,
                                "Stop Time": stop.stop_time if hasattr(stop, 'stop_time') else None,
                                "Resume Time": stop.resume_time if hasattr(stop, 'resume_time') else None,
                                "Start Time": stop.start_time if hasattr(stop, 'start_time') else None,
                                "Stop Duration (min)": stop_duration,
                                "Liters Added": stop.liters_added if hasattr(stop, 'liters_added') else 0,
                                "KM Reading": stop.current_km if hasattr(stop, 'current_km') else 0,
                                "Location Stop (Lat, Long)": f"{stop.Latitude_stop}, {stop.Longitude_stop}" if hasattr(stop, 'Latitude_stop') and hasattr(stop, 'Longitude_stop') else "",
                                "Location Start (Lat, Long)": f"{stop.Latitude_start}, {stop.Longitude_start}" if hasattr(stop, 'Latitude_start') and hasattr(stop, 'Longitude_start') and stop.Latitude_start and stop.Longitude_start else ""
                            }
                            fuel_stops_data.append(stop_data)
                        
                        fuel_stops_df = pd.DataFrame(fuel_stops_data)
                        fuel_stops_df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Return to beginning of file
        output.seek(0)
        return output 