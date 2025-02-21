from src.controllers.stock_controllers import get_daily_stock
from src.controllers.storage_controllers import get_storage_by_branch
from src.controllers.product_controllers import get_product_by_company
from src.services.whatsapp_service import upload_file_to_whatsapp, send_whatsapp_message_with_file
from flask import jsonify, request
from datetime import date
import xlsxwriter
import pandas as pd
import logging
import io

def create_stock_report(stocks, storages, products):  
    data = []

    # Convertir storages y products a diccionarios para búsquedas más rápidas
    storage_dict = {s.id_storage: s for s in storages}
    product_dict = {p.id_product: p for p in products}

    for stock in stocks:
        storage = storage_dict.get(stock.id_storage)
        product = product_dict.get(stock.id_product)

        #aqui obtener producto
        data.append({
            'ID Almacen' : stock.id_storage,
            'Almacen' : storage.name if storage else 'Almacén no encontrado',
            'ID Producto': stock.id_product,
            'Producto': product.description if product else 'Producto no encontrado',
            'Cantidad' : stock.stock,
            'Fecha de ingreso' : stock.entry_date
        })
    
    df = pd.DataFrame(data)
    output = io.BytesIO()

    today = date.today()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Exportar DataFrame a Excel
        df.to_excel(writer, index=False, sheet_name=f'stock_diario_{today}')

        # Obtener el workbook y worksheet para formato
        workbook = writer.book
        worksheet = writer.sheets[f'stock_diario_{today}']

        # Establecer anchos de columna
        column_widths = {
            'A': 12,  # ID Almacen
            'B': 20,  # Almacen
            'C': 12,  # ID Producto
            'D': 40,  # Producto
            'E': 10,  # Cantidad
            'F': 20   # Fecha de ingreso
        }

        for col, width in column_widths.items():
            worksheet.set_column(f'{col}:{col}', width)
        
        # Agregar formato al encabezado
        header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#D9EAD3',  # Color de fondo
            'border': 1
        })
        
        for col_num, value in enumerate(df.columns):
            worksheet.write(0, col_num, value, header_format)
    
    output.seek(0)
    return output

def send_daily_sales_report_whatsapp(idCompany, idBranch, whatsappPhoneDestination, whatsappPhoneNumberId, whatsappToken):
    try:
        # Obtengo storages
        storages = get_storage_by_branch(idBranch)

        # Obtener las órdenes del día
        stocks = get_daily_stock(storages)

        # Obtengo los productos de la empresa
        products = get_product_by_company(idCompany)

        # Crear el reporte en Excel
        report = create_stock_report(stocks, storages, products)

        # Subir el archivo Excel a WhatsApp
        today = date.today()
        file_name = f'stock_diario_{today}.xlsx'
        mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        media_id = upload_file_to_whatsapp(report, file_name, mime_type, whatsappPhoneNumberId, whatsappToken)

        # Enviar el archivo adjunto por WhatsApp
        type_document = "document"
        caption = f"stock_diario_{today}"
        file_name = f"stock_diario_{today}.xlsx"
        send_whatsapp_message_with_file(media_id, type_document, caption, file_name, f'whatsapp:+{whatsappPhoneDestination}', whatsappPhoneNumberId, whatsappToken)
        #send_whatsapp_message_with_file(media_id, type_document, caption, file_name, f'whatsapp:+59175002433', whatsappPhoneNumberId, whatsappToken)

        logging.info("Reporte diario enviado exitosamente")
        return jsonify({'status': 'Reporte diario enviado exitosamente'}), 200
    except Exception as e:
        logging.error(f"Error al enviar el reporte diario: {e}")
        return jsonify({"error": f"Ocurrio un error al enviar el reporte diario: {str(e)}"}), 500