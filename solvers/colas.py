import re
import math

def resolver_colas(texto):
    try:
        texto_lower = texto.lower()
        
        # Buscar lambda (λ) o tasa de llegada
        lam_match = re.search(r'(?:lambda|λ|tasa de llegada)\s*[\(\)=:]*\s*(?:\()?(?:lambda)?(?:\))?\s*[=:]\s*([\d,\.]+)', texto_lower)
        
        # Buscar mu (μ) o tasa de servicio
        mu_match = re.search(r'(?:mu|μ|tasa de servicio)\s*[\(\)=:]*\s*(?:\()?(?:mu)?(?:\))?\s*[=:]\s*([\d,\.]+)', texto_lower)
        
        if not (lam_match and mu_match):
            return "⚠️ No se encontraron λ (tasa de llegada) y μ (tasa de servicio)"
        
        lam = float(lam_match.group(1).replace(',', ''))
        mu = float(mu_match.group(1).replace(',', ''))
        
        if lam <= 0 or mu <= 0:
            return "⚠️ Las tasas deben ser positivas"
        
        if lam >= mu:
            return f"⚠️ Sistema inestable (λ={lam} >= μ={mu}). La cola crece indefinidamente."
        
        # Calcular métricas M/M/1
        rho = lam / mu  # Utilización del servidor
        L = lam / (mu - lam)  # Clientes en el sistema
        Lq = (lam ** 2) / (mu * (mu - lam))  # Clientes en cola
        W = 1 / (mu - lam)  # Tiempo en sistema (horas)
        Wq = lam / (mu * (mu - lam))  # Tiempo en cola (horas)
        P0 = 1 - rho  # Probabilidad de sistema vacío
        
        # Convertir W a minutos si es apropiado
        W_minutos = W * 60
        Wq_minutos = Wq * 60
        
        # Probabilidad de tener n clientes
        Pn_formula = f"P(n) = (1 - ρ) * ρ^n = {P0:.4f} * {rho:.4f}^n"
        
        resultado = f"""☎️ TEORÍA DE COLAS (Modelo M/M/1)

Parámetros:
- Tasa de llegada (λ): {lam:.2f} clientes/hora
- Tasa de servicio (μ): {mu:.2f} clientes/hora

Métricas del Sistema:
- Utilización del servidor (ρ = λ/μ): {rho:.1%}
- Clientes en el sistema (L): {L:.2f} clientes
- Clientes en cola (Lq): {Lq:.2f} clientes
- Tiempo en sistema (W): {W:.4f} horas = {W_minutos:.1f} minutos
- Tiempo en cola (Wq): {Wq:.4f} horas = {Wq_minutos:.1f} minutos
- Probabilidad de sistema vacío (P₀): {P0:.1%}

Fórmulas utilizadas:
- ρ = λ/μ
- L = λ/(μ - λ)
- Lq = λ²/[μ(μ - λ)]
- W = 1/(μ - λ)
- Wq = λ/[μ(μ - λ)]
- {Pn_formula}
"""
        
        return resultado
    
    except Exception as e:
        return f"⚠️ Error en cálculo de colas: {str(e)}"