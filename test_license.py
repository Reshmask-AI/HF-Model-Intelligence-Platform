from app.services.license_service import get_license_intelligence

license_info = get_license_intelligence("apache-2.0")

print(license_info)