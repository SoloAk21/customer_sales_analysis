from odoo import models, fields

class ReportSaleAnalysis(models.AbstractModel):
    _name = 'report.customer_sales_analysis.report_sales_analysis'
    _description = 'Sales Analysis Report'

    def _get_report_values(self, docids, data=None):
        partner = self.env['res.partner'].browse(docids)
        orders = self.env['sale.order'].search([
            ('partner_id', '=', partner.id),
            ('state', 'in', ['sale', 'done'])
        ])
        sales_data = self.env['sale.order.line'].read_group(
            [('order_id', 'in', orders.ids)],
            ['price_total', 'product_uom_qty', 'product_id'],
            ['product_id'],
            lazy=False
        )
        report_lines = []
        total_sales = 0.0
        category_data = {}
        for group in sales_data:
            product = self.env['product.product'].browse(group['product_id'][0])
            category = product.categ_id.name if product.categ_id else 'Uncategorized'
            category_id = product.categ_id.id if product.categ_id else False
            if category not in category_data:
                category_data[category] = {
                    'category_id': category_id,
                    'products': [],
                    'category_total': 0.0
                }
            category_data[category]['products'].append({
                'name': product.name,
                'quantity': group['product_uom_qty'],
                'total': group['price_total']
            })
            category_data[category]['category_total'] += group['price_total']
            total_sales += group['price_total']

        for category, data in category_data.items():
            report_lines.append({
                'category': category,
                'products': data['products'],
                'category_total': data['category_total']
            })

        # Use main company's currency if partner's company currency is unset
        currency = partner.company_id.currency_id or self.env.company.currency_id

        return {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'docs': partner,
            'data': data or {},
            'report_lines': report_lines,
            'total_sales': total_sales,
            'currency_id': currency,
        }