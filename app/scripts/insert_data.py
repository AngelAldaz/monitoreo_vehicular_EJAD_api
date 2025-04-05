from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.brandsModel import Brand
from app.models.modelsModel import Model
from app.models.descriptionsModel import Description

def insert_data():
    # Crear una sesión de base de datos
    db = SessionLocal()
    
    try:
        # Verificar si ya hay datos en las tablas para evitar duplicados
        existing_brands = db.query(Brand).count()
        if existing_brands > 0:
            print("Ya existen datos en la base de datos. No se insertarán datos duplicados.")
            return
        
        # 1. Insertar marcas
        brands = [
            Brand(name="Toyota"),
            Brand(name="Honda"),
            Brand(name="Nissan"),
            Brand(name="Chevrolet"),
            Brand(name="Ford"),
            Brand(name="Volkswagen"),
            Brand(name="Hyundai"),
            Brand(name="Mazda"),
            Brand(name="Kia"),
            Brand(name="Mercedes-Benz")
        ]
        
        db.add_all(brands)
        db.commit()
        
        # Refrescar objetos para obtener IDs
        for brand in brands:
            db.refresh(brand)
        
        print(f"Se han insertado {len(brands)} marcas de vehículos")
        
        # 2. Insertar modelos
        models = [
            # Toyota (id_brand = 1)
            Model(name="Corolla", id_brand_fk=brands[0].id_brand),
            Model(name="Camry", id_brand_fk=brands[0].id_brand),
            Model(name="RAV4", id_brand_fk=brands[0].id_brand),
            Model(name="Hilux", id_brand_fk=brands[0].id_brand),
            # Honda (id_brand = 2)
            Model(name="Civic", id_brand_fk=brands[1].id_brand),
            Model(name="Accord", id_brand_fk=brands[1].id_brand),
            Model(name="CR-V", id_brand_fk=brands[1].id_brand),
            # Nissan (id_brand = 3)
            Model(name="Sentra", id_brand_fk=brands[2].id_brand),
            Model(name="Altima", id_brand_fk=brands[2].id_brand),
            Model(name="X-Trail", id_brand_fk=brands[2].id_brand),
            Model(name="Frontier", id_brand_fk=brands[2].id_brand),
            # Chevrolet (id_brand = 4)
            Model(name="Spark", id_brand_fk=brands[3].id_brand),
            Model(name="Cruze", id_brand_fk=brands[3].id_brand),
            Model(name="Silverado", id_brand_fk=brands[3].id_brand),
            # Ford (id_brand = 5)
            Model(name="Focus", id_brand_fk=brands[4].id_brand),
            Model(name="Ranger", id_brand_fk=brands[4].id_brand),
            Model(name="Explorer", id_brand_fk=brands[4].id_brand),
            # Volkswagen (id_brand = 6)
            Model(name="Golf", id_brand_fk=brands[5].id_brand),
            Model(name="Jetta", id_brand_fk=brands[5].id_brand),
            Model(name="Tiguan", id_brand_fk=brands[5].id_brand),
            # Otros modelos para las demás marcas
            Model(name="Tucson", id_brand_fk=brands[6].id_brand),
            Model(name="CX-5", id_brand_fk=brands[7].id_brand),
            Model(name="Sportage", id_brand_fk=brands[8].id_brand),
            Model(name="Clase C", id_brand_fk=brands[9].id_brand)
        ]
        
        db.add_all(models)
        db.commit()
        
        # Refrescar objetos para obtener IDs
        for model in models:
            db.refresh(model)
            
        print(f"Se han insertado {len(models)} modelos de vehículos")
        
        # 3. Insertar descripciones
        descriptions = [
            # Toyota Corolla (id_model = 1)
            Description(name="Corolla LE 1.8L", id_model_fk=models[0].id_model),
            Description(name="Corolla SE 2.0L", id_model_fk=models[0].id_model),
            # Toyota Camry (id_model = 2)
            Description(name="Camry LE 2.5L", id_model_fk=models[1].id_model),
            Description(name="Camry XSE V6", id_model_fk=models[1].id_model),
            # Toyota RAV4 (id_model = 3)
            Description(name="RAV4 LE 2.5L", id_model_fk=models[2].id_model),
            Description(name="RAV4 XLE Hybrid", id_model_fk=models[2].id_model),
            # Toyota Hilux (id_model = 4)
            Description(name="Hilux SR 2.4L Diesel", id_model_fk=models[3].id_model),
            Description(name="Hilux SRV 2.8L 4x4", id_model_fk=models[3].id_model),
            # Honda Civic (id_model = 5)
            Description(name="Civic DX Sedan", id_model_fk=models[4].id_model),
            Description(name="Civic EX-L Turbo", id_model_fk=models[4].id_model),
            # Honda Accord (id_model = 6)
            Description(name="Accord Sport 1.5T", id_model_fk=models[5].id_model),
            Description(name="Accord Touring 2.0T", id_model_fk=models[5].id_model),
            # Honda CR-V (id_model = 7)
            Description(name="CR-V LX AWD", id_model_fk=models[6].id_model),
            Description(name="CR-V Touring AWD", id_model_fk=models[6].id_model),
            # Nissan Sentra (id_model = 8)
            Description(name="Sentra SR 2.0L", id_model_fk=models[7].id_model),
            Description(name="Sentra Exclusive CVT", id_model_fk=models[7].id_model),
            # Otros modelos
            Description(name="Altima S 2.5L", id_model_fk=models[8].id_model),
            Description(name="X-Trail Advance", id_model_fk=models[9].id_model),
            Description(name="Frontier LE 4x4", id_model_fk=models[10].id_model),
            Description(name="Spark LT MT", id_model_fk=models[11].id_model),
            Description(name="Cruze Premier", id_model_fk=models[12].id_model),
            Description(name="Silverado LTZ", id_model_fk=models[13].id_model),
            Description(name="Focus Titanium", id_model_fk=models[14].id_model),
            Description(name="Ranger XLT 4x4", id_model_fk=models[15].id_model),
            Description(name="Explorer Limited", id_model_fk=models[16].id_model),
            Description(name="Golf Comfortline", id_model_fk=models[17].id_model),
            Description(name="Jetta GLI", id_model_fk=models[18].id_model),
            Description(name="Tiguan Trendline", id_model_fk=models[19].id_model),
            Description(name="Tucson GLS", id_model_fk=models[20].id_model),
            Description(name="CX-5 Grand Touring", id_model_fk=models[21].id_model),
            Description(name="Sportage EX", id_model_fk=models[22].id_model),
            Description(name="Clase C 200 AMG Line", id_model_fk=models[23].id_model)
        ]
        
        db.add_all(descriptions)
        db.commit()
        
        print(f"Se han insertado {len(descriptions)} descripciones de vehículos")
        print("Inserción de datos completada con éxito!")
        
    except Exception as e:
        db.rollback()
        print(f"Error al insertar datos: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    insert_data()