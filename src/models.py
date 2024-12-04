import os
import sys
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base, backref
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

# Tabla Usuario
class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    subscription_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relación con los favoritos
    favoritos = relationship('Favoritos', backref='usuario')

# Tabla Planeta
class Planeta(Base):
    __tablename__ = 'planetas'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    climate = Column(String)
    population = Column(String)
    terrain = Column(String)
    
    # Relación con los favoritos
    favoritos = relationship('Favoritos', backref='planeta')

# Tabla Personaje
class Personaje(Base):
    __tablename__ = 'personajes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    species = Column(String)
    gender = Column(String)
    homeworld_id = Column(Integer, ForeignKey('planetas.id'))
    
    homeworld = relationship('Planeta')
    
    # Relación con los favoritos
    favoritos = relationship('Favoritos', backref='personaje')

# Tabla Favoritos (tabla intermedia)
class Favoritos(Base):
    __tablename__ = 'favoritos'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('usuarios.id'))
    planet_id = Column(Integer, ForeignKey('planetas.id'), nullable=True)
    character_id = Column(Integer, ForeignKey('personajes.id'), nullable=True)
    
    # Relaciones con usuario, planeta y personaje
    usuario = relationship('Usuario', backref=backref('favoritos_usuario', lazy='dynamic'))
    planeta = relationship('Planeta', backref=backref('favoritos_planeta', lazy='dynamic'))
    personaje = relationship('Personaje', backref=backref('favoritos_personaje', lazy='dynamic'))

# Crear la base de datos
engine = create_engine('sqlite:///starwars_blog.db')
Base.metadata.create_all(engine)

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
