USE [DatosColombiaDB26]
GO

CREATE TABLE [dbo].[usuarios](
    [id] [int] IDENTITY(1,1) NOT NULL,
    [usuario] [varchar](50) NOT NULL UNIQUE,
    [contrasena] [varchar](50) NOT NULL,
    PRIMARY KEY CLUSTERED ([id] ASC)
) ON [PRIMARY];
GO

-- Insertamos el usuario administrador por defecto
INSERT INTO [dbo].[usuarios] (usuario, contrasena) 
VALUES ('admin', 'admin123');
GO