from app.schemas import EngineeringGraph, PropertyValuationResponse

# Mock dataset for Hong Kong district property prices and rents
# Source: FlowDraft demo context
HK_DISTRICT_DATA = {
    "Kwun Tong": {
        "price_per_sqm": 80000.0,
        "rent_per_sqm_per_month": 300.0,
    },
    "Tsuen Wan": {
        "price_per_sqm": 70000.0,
        "rent_per_sqm_per_month": 250.0,
    },
    "Central": {
        "price_per_sqm": 200000.0,
        "rent_per_sqm_per_month": 800.0,
    },
    "Sha Tin": {
        "price_per_sqm": 60000.0,
        "rent_per_sqm_per_month": 200.0,
    },
}


def derive_total_area(graph: EngineeringGraph) -> float:
    """Derive total area in sqm from graph meta or spaces."""

    # Check meta properties first
    if "total_area" in graph.meta.properties:
        try:
            return float(graph.meta.properties["total_area"])
        except (ValueError, TypeError):
            pass

    # Fallback to summing up spaces area
    total_area = 0.0
    for space in graph.spaces:
        if space.area is not None:
            total_area += space.area

    return total_area


def calculate_property_valuation(
    graph: EngineeringGraph, district: str
) -> PropertyValuationResponse:
    """Calculate property valuation based on graph area and district data."""

    # Normalize district
    normalized_district = district.strip()

    if normalized_district not in HK_DISTRICT_DATA:
        raise ValueError(f"Unknown district: {normalized_district}")

    district_data = HK_DISTRICT_DATA[normalized_district]

    # Calculate area
    total_area_sqm = derive_total_area(graph)

    if total_area_sqm <= 0:
        raise ValueError("Total area could not be derived from graph or is zero.")

    # Calculate values
    price_per_sqm = district_data["price_per_sqm"]
    rent_per_sqm_per_month = district_data["rent_per_sqm_per_month"]

    estimated_value_hkd = total_area_sqm * price_per_sqm
    estimated_monthly_rent_hkd = total_area_sqm * rent_per_sqm_per_month

    # Calculate ROI
    estimated_annual_rent_hkd = estimated_monthly_rent_hkd * 12

    estimated_roi_percentage = 0.0
    if estimated_value_hkd > 0:
        estimated_roi_percentage = (estimated_annual_rent_hkd / estimated_value_hkd) * 100.0

    assumptions = [
        f"District: {normalized_district}",
        f"Price per sqm: HKD {price_per_sqm:,.2f}",
        f"Rent per sqm per month: HKD {rent_per_sqm_per_month:,.2f}",
        "ROI is based on 100% occupancy and does not account for operational costs or taxes.",
    ]

    return PropertyValuationResponse(
        total_area_sqm=round(total_area_sqm, 2),
        estimated_value_hkd=round(estimated_value_hkd, 2),
        estimated_monthly_rent_hkd=round(estimated_monthly_rent_hkd, 2),
        estimated_roi_percentage=round(estimated_roi_percentage, 2),
        assumptions=assumptions,
        dataset_provenance="FlowDraft Hong Kong Property Demo Dataset",
    )
