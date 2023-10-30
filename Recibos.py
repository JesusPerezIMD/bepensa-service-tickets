#The prebuilt-receipt model extracts key information from printed and handwritten sales receipts.

#Tipos de recibo: https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept-receipt?view=doc-intel-3.1.0#receipt
def analizar_ticket(url):
    """
    This code sample shows Prebuilt Receipt operations with the Azure Form Recognizer client library. 
    The async versions of the samples require Python 3.6 or later.

    To learn more, please visit the documentation - Quickstart: Form Recognizer Python client library SDKs
    https://docs.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/quickstarts/try-v3-python-sdk
    """

    from azure.core.credentials import AzureKeyCredential
    from azure.ai.formrecognizer import DocumentAnalysisClient

    """
    Remember to remove the key from your code when you're done, and never post it publicly. For production, use
    secure methods to store and access your credentials. For more information, see 
    https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-security?tabs=command-line%2Ccsharp#environment-variables-and-application-configuration
    """
    endpoint = "https://citcognitiveservicedev.cognitiveservices.azure.com"
    key = "586bf736a33a4b8b8795ddd9d4aeb2e7"

    # imagen ejemplo : https://bepensacitdev.blob.core.windows.net/searchcontainerdev/20231017_115619 (2).jpg
    #https://bepensacitdev.blob.core.windows.net/searchcontainerdev/20231018_171438.jpg
    url = url

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-receipt", url)
    receipts = poller.result()

    for idx, receipt in enumerate(receipts.documents):
        print("--------Reconociendo recibo #{}--------".format(idx + 1))
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
                "Fecha de emisiÃ³n del recibo: {} con confianza: {}".format(
                    transaction_date.value, transaction_date.confidence
                )
            )
        if receipt.fields.get("Items"):
            print("ArtÃ­culos:")
            for idx, item in enumerate(receipt.fields.get("Items").value):
                print("...ArtÃ­culo #{}".format(idx + 1))
                item_description = item.value.get("Description")
                if item_description:
                    print(
                        "......DescripciÃ³n: {} con confianza: {}".format(
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
    url = str(input("Por favor ingresa la url de la imagen a analizar: "))
    analizar_ticket(url)