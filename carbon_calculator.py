from typing import Dict, Any
import math

class CarbonCalculator:
    """Calculates estimated carbon footprint and energy consumption of code"""
    
    def __init__(self):
        # Energy consumption estimates (in micro-joules per operation)
        self.energy_costs = {
            'function_call': 0.5,
            'while_loop_iteration': 2.0,
            'for_loop_iteration': 1.5,
            'list_comprehension': 1.0,
            'import_statement': 0.3,
            'memory_allocation': 0.8,
            'string_operation': 0.2,
            'math_operation': 0.1
        }
        
        # Carbon emission factor (grams CO2 per kWh) - average global grid
        self.carbon_factor = 500  # grams CO2 per kWh
        
        # Conversion factor: micro-joules to kWh
        self.uj_to_kwh = 2.78e-13
    
    def calculate_energy_consumption(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate estimated energy consumption based on code analysis"""
        
        # Base energy for code execution
        lines_of_code = analysis_results.get('lines_of_code', 0)
        base_energy = lines_of_code * 0.1  # Base energy per line
        
        # Additional energy costs
        function_energy = analysis_results.get('function_count', 0) * self.energy_costs['function_call']
        while_loop_energy = analysis_results.get('while_loop_count', 0) * self.energy_costs['while_loop_iteration'] * 10  # Assuming 10 iterations
        for_loop_energy = analysis_results.get('for_loop_count', 0) * self.energy_costs['for_loop_iteration'] * 10
        import_energy = analysis_results.get('import_count', 0) * self.energy_costs['import_statement']
        
        # Inefficiency penalties
        issues = analysis_results.get('issues', [])
        inefficiency_energy = 0
        
        for issue in issues:
            if issue['type'] == 'while_loop':
                inefficiency_energy += 5.0  # Extra energy for inefficient while loops
            elif issue['type'] == 'inefficient_range_len':
                inefficiency_energy += 2.0  # Extra energy for range(len()) patterns
            elif issue['type'] == 'unused_import':
                inefficiency_energy += 0.5  # Energy wasted on unused imports
        
        total_energy = (base_energy + function_energy + while_loop_energy + 
                       for_loop_energy + import_energy + inefficiency_energy)
        
        return {
            'total_energy_uj': total_energy,
            'base_energy': base_energy,
            'function_energy': function_energy,
            'loop_energy': while_loop_energy + for_loop_energy,
            'import_energy': import_energy,
            'inefficiency_penalty': inefficiency_energy,
            'energy_breakdown': {
                'Base Execution': base_energy,
                'Functions': function_energy,
                'Loops': while_loop_energy + for_loop_energy,
                'Imports': import_energy,
                'Inefficiencies': inefficiency_energy
            }
        }
    
    def calculate_carbon_footprint(self, energy_consumption: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate carbon footprint from energy consumption"""
        
        total_energy_uj = energy_consumption['total_energy_uj']
        total_energy_kwh = total_energy_uj * self.uj_to_kwh
        
        # Carbon emissions in grams
        carbon_emissions_g = total_energy_kwh * self.carbon_factor
        
        # Convert to more readable units
        if carbon_emissions_g < 0.001:
            carbon_display = f"{carbon_emissions_g * 1000:.3f} mg"
        elif carbon_emissions_g < 1:
            carbon_display = f"{carbon_emissions_g:.3f} g"
        else:
            carbon_display = f"{carbon_emissions_g:.2f} g"
        
        return {
            'carbon_emissions_g': carbon_emissions_g,
            'carbon_display': carbon_display,
            'energy_kwh': total_energy_kwh,
            'equivalent_metrics': self._calculate_equivalents(carbon_emissions_g)
        }
    
    def _calculate_equivalents(self, carbon_g: float) -> Dict[str, str]:
        """Calculate equivalent carbon emissions for context"""
        
        # Equivalents in grams CO2
        equivalents = {}
        
        # Smartphone charging (approximately 5g CO2)
        smartphone_charge = carbon_g / 5.0
        if smartphone_charge > 0.001:
            equivalents['smartphone_charges'] = f"{smartphone_charge:.3f} smartphone charges"
        
        # Car driving (approximately 150g CO2 per km)
        car_meters = (carbon_g / 150.0) * 1000
        if car_meters > 0.1:
            equivalents['car_driving'] = f"{car_meters:.1f} meters of car driving"
        
        # LED bulb usage (approximately 0.5g CO2 per hour)
        led_hours = carbon_g / 0.5
        if led_hours > 0.01:
            equivalents['led_bulb_hours'] = f"{led_hours:.2f} hours of LED bulb usage"
        
        return equivalents
    
    def calculate_optimization_savings(self, original_analysis: Dict[str, Any], 
                                     optimized_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate potential savings from code optimization"""
        
        original_energy = self.calculate_energy_consumption(original_analysis)
        optimized_energy = self.calculate_energy_consumption(optimized_analysis)
        
        energy_saved = original_energy['total_energy_uj'] - optimized_energy['total_energy_uj']
        
        original_carbon = self.calculate_carbon_footprint(original_energy)
        optimized_carbon = self.calculate_carbon_footprint(optimized_energy)
        
        carbon_saved = original_carbon['carbon_emissions_g'] - optimized_carbon['carbon_emissions_g']
        
        # Calculate percentage savings
        energy_reduction_percent = (energy_saved / original_energy['total_energy_uj']) * 100 if original_energy['total_energy_uj'] > 0 else 0
        carbon_reduction_percent = (carbon_saved / original_carbon['carbon_emissions_g']) * 100 if original_carbon['carbon_emissions_g'] > 0 else 0
        
        return {
            'energy_saved_uj': energy_saved,
            'carbon_saved_g': carbon_saved,
            'energy_reduction_percent': energy_reduction_percent,
            'carbon_reduction_percent': carbon_reduction_percent,
            'original_consumption': original_energy,
            'optimized_consumption': optimized_energy,
            'original_carbon': original_carbon,
            'optimized_carbon': optimized_carbon,
            'savings_equivalents': self._calculate_equivalents(carbon_saved) if carbon_saved > 0 else {}
        }
    
    def get_efficiency_rating(self, analysis_results: Dict[str, Any]) -> str:
        """Get energy efficiency rating for the code"""
        
        energy_data = self.calculate_energy_consumption(analysis_results)
        lines_of_code = analysis_results.get('lines_of_code', 1)
        
        # Calculate energy per line of code
        energy_per_line = energy_data['total_energy_uj'] / lines_of_code
        
        # Rating scale based on energy efficiency
        if energy_per_line <= 0.2:
            return "A++ (Extremely Efficient)"
        elif energy_per_line <= 0.5:
            return "A+ (Very Efficient)"
        elif energy_per_line <= 1.0:
            return "A (Efficient)"
        elif energy_per_line <= 2.0:
            return "B (Moderately Efficient)"
        elif energy_per_line <= 5.0:
            return "C (Below Average)"
        elif energy_per_line <= 10.0:
            return "D (Inefficient)"
        else:
            return "F (Very Inefficient)"
    
    def generate_carbon_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate a comprehensive carbon footprint report"""
        
        energy_data = self.calculate_energy_consumption(analysis_results)
        carbon_data = self.calculate_carbon_footprint(energy_data)
        efficiency_rating = self.get_efficiency_rating(analysis_results)
        
        report_lines = [
            "🌍 CARBON FOOTPRINT ANALYSIS",
            "=" * 40,
            f"Energy Consumption: {energy_data['total_energy_uj']:.2f} μJ",
            f"Carbon Emissions: {carbon_data['carbon_display']}",
            f"Efficiency Rating: {efficiency_rating}",
            "",
            "📊 ENERGY BREAKDOWN:",
        ]
        
        for category, energy in energy_data['energy_breakdown'].items():
            percentage = (energy / energy_data['total_energy_uj']) * 100 if energy_data['total_energy_uj'] > 0 else 0
            report_lines.append(f"  {category}: {energy:.2f} μJ ({percentage:.1f}%)")
        
        if carbon_data['equivalent_metrics']:
            report_lines.extend([
                "",
                "🌱 ENVIRONMENTAL CONTEXT:",
            ])
            for metric, value in carbon_data['equivalent_metrics'].items():
                report_lines.append(f"  Equivalent to: {value}")
        
        return "\n".join(report_lines)