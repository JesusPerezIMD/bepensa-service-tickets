
def analizar_ticket(url):

    from azure.core.credentials import AzureKeyCredential
    from azure.ai.formrecognizer import DocumentAnalysisClient

    endpoint = "https://citcognitiveservicedev.cognitiveservices.azure.com"
    key = "586bf736a33a4b8b8795ddd9d4aeb2e7"

    url = url

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-receipt", url)
    receipts = poller.result()

    for idx, receipt in enumerate(receipts.documents):
        print("--------Reconociendo Recibo #{}--------".format(idx + 1))
        receipt_type = receipt.doc_type
        if receipt_type:
            print(
                "Tipo de recibo: {}".format(receipt_type)
            )
        merchant_name = receipt.fields.get("MerchantName")
        if merchant_name:
            print(
                "Nombre del comerciante: {} con int. de confianza: {}".format(
                    merchant_name.value, merchant_name.confidence
                )
            )
        transaction_date = receipt.fields.get("TransactionDate")
        if transaction_date:
            print(
                "Fecha de emisión del recibo: {} con confianza: {}".format(
                    transaction_date.value, transaction_date.confidence
                )
            )
        if receipt.fields.get("Items"):
            print("Artículos:")
            for idx, item in enumerate(receipt.fields.get("Items").value):
                print("...Artículo #{}".format(idx + 1))
                item_description = item.value.get("Description")
                if item_description:
                    print(
                        "......Descripción: {} con confianza: {}".format(
                            item_description.value, item_description.confidence
                        )
                    )
                item_quantity = item.value.get("Quantity")
                if item_quantity:
                    print(
                        "......Cantidad: {} con confianza: {}".format(
                            item_quantity.value, item_quantity.confidence
                        )
                    )
                item_price = item.value.get("Price")
                if item_price:
                    print(
                        "......Precio individual: ${} con  confianza: {}".format(
                            item_price.value, item_price.confidence
                        )
                    )
                item_total_price = item.value.get("TotalPrice")
                if item_total_price:
                    print(
                        "......Precio total: ${} con confianza: {}".format(
                            item_total_price.value, item_total_price.confidence
                        )
                    )
        subtotal = receipt.fields.get("Subtotal")
        if subtotal:
            print(
                "Subtotal: {} con confianza: {}".format(
                    subtotal.value, subtotal.confidence
                )
            )
        tax = receipt.fields.get("TotalTax")
        if tax:
            print("Impuestos: ${} con confianza {}".format(tax.value, tax.confidence))
        tip = receipt.fields.get("Tip")
        if tip:
            print("Propina: ${} con confianza: {}".format(tip.value, tip.confidence))
        total = receipt.fields.get("Total")
        if total:
            print("Total: ${} con  confianza: {}".format(total.value, total.confidence))
        print("--------------------------------------")

if __name__ == "__main__":
    print(">BEPENSA-SERVICE-TICKETS<")
    print("--------------------------------------")
    url = str(input("+URL: "))
    analizar_ticket(url)