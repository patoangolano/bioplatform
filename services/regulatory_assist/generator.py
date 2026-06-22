"""Gerador de esqueletos de documentos regulatórios GxP.

Gera documentos estruturados conforme ICH E6(R2) e requisitos Anvisa (RDC 9/2015).
Seções geradas por IA são marcadas com proveniência explícita.
"""

from datetime import datetime

from .models import DocumentType, RegulatoryDocument, RegulatoryRequest, Section

_PROVENANCE_NOTICE = (
    "[GERADO POR IA] Este conteúdo foi gerado automaticamente pela plataforma bioplatform "
    "e requer revisão por profissional qualificado antes de uso regulatório."
)


def _metadata(request: RegulatoryRequest) -> dict:
    """Gera metadados comuns de proveniência."""
    return {
        "generator": "bioplatform/regulatory_assist",
        "generator_version": "0.1.0",
        "ai_generated": True,
        "provenance_notice": _PROVENANCE_NOTICE,
        "sponsor": request.sponsor,
        "principal_investigator": request.principal_investigator,
        "therapeutic_area": request.therapeutic_area,
        "phase": request.phase,
        "regulatory_framework": ["ICH E6(R2)", "RDC 9/2015 (Anvisa)"],
    }


def generate_protocol_skeleton(request: RegulatoryRequest) -> RegulatoryDocument:
    """Gera esqueleto de protocolo clínico conforme ICH E6(R2) e Anvisa."""
    sections = [
        Section(
            number="1",
            title="Informações Gerais",
            content=(
                f"Título do estudo: {request.study_title}\n"
                f"Patrocinador: {request.sponsor}\n"
                f"Investigador principal: {request.principal_investigator}\n"
                f"Fase: {request.phase}\n"
                f"Área terapêutica: {request.therapeutic_area}\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=["ICH E6(R2) Seção 6", "RDC 9/2015 Art. 4º"],
        ),
        Section(
            number="2",
            title="Introdução e Racional",
            content=(
                "[INSERIR] Contexto científico, justificativa do estudo e revisão "
                "da literatura relevante para a área terapêutica.\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=["ICH E6(R2) Seção 6.2"],
        ),
        Section(
            number="3",
            title="Objetivos e Desfechos",
            content=(
                "Objetivo primário: [INSERIR]\n"
                "Objetivos secundários: [INSERIR]\n\n"
                "Desfechos:\n"
                + "\n".join(f"  - {ep}" for ep in request.endpoints)
                + f"\n\n{_PROVENANCE_NOTICE}"
            ),
            references=["ICH E6(R2) Seção 6.3"],
        ),
        Section(
            number="4",
            title="Desenho do Estudo",
            content=(
                f"Estudo de fase {request.phase}.\n"
                "Desenho: [INSERIR randomizado/aberto/duplo-cego/etc.]\n"
                "Duração: [INSERIR]\n"
                "Braços de tratamento: [INSERIR]\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=["ICH E6(R2) Seção 6.4", "RDC 9/2015 Art. 5º"],
        ),
        Section(
            number="5",
            title="Seleção e Retirada de Sujeitos",
            content=(
                f"Critérios de inclusão/exclusão:\n{request.population_criteria}\n\n"
                "Critérios de retirada: [INSERIR]\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=["ICH E6(R2) Seção 6.5", "RDC 9/2015 Art. 8º"],
        ),
        Section(
            number="6",
            title="Tratamento dos Sujeitos",
            content=(
                "Produto investigacional: [INSERIR]\n"
                "Posologia e via de administração: [INSERIR]\n"
                "Medicamentos concomitantes permitidos/proibidos: [INSERIR]\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=["ICH E6(R2) Seção 6.6"],
        ),
        Section(
            number="7",
            title="Avaliação de Eficácia",
            content=(
                "Métodos de avaliação dos desfechos: [INSERIR]\n"
                "Cronograma de avaliações: [INSERIR]\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=["ICH E6(R2) Seção 6.7"],
        ),
        Section(
            number="8",
            title="Avaliação de Segurança",
            content=(
                "Parâmetros de segurança: [INSERIR]\n"
                "Definição e reporte de eventos adversos: [INSERIR]\n"
                "Procedimento para SAE/SUSAR: conforme RDC 9/2015 Art. 28.\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=["ICH E6(R2) Seção 6.8", "RDC 9/2015 Art. 28"],
        ),
        Section(
            number="9",
            title="Estatística",
            content=(
                "Tamanho amostral: [INSERIR justificativa]\n"
                "Análise primária: [INSERIR]\n"
                "Populações de análise (ITT, PP): [INSERIR]\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=["ICH E6(R2) Seção 6.9", "ICH E9"],
        ),
        Section(
            number="10",
            title="Considerações Éticas",
            content=(
                "O estudo será conduzido conforme a Declaração de Helsinque, "
                "ICH-GCP e legislação brasileira vigente (Res. CNS 466/2012, "
                "RDC 9/2015).\n"
                "Aprovação do CEP/CONEP: [INSERIR]\n"
                "Registro no REBEC: [INSERIR]\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=[
                "ICH E6(R2) Seção 6.10",
                "RDC 9/2015 Art. 10",
                "Res. CNS 466/2012",
            ],
        ),
    ]

    return RegulatoryDocument(
        document_type=DocumentType.PROTOCOL,
        title=f"Protocolo Clínico — {request.study_title}",
        sections=sections,
        metadata=_metadata(request),
        generated_at=datetime.utcnow(),
        version="0.1-draft",
    )


def generate_sap_skeleton(request: RegulatoryRequest) -> RegulatoryDocument:
    """Gera esqueleto de Plano de Análise Estatística conforme ICH E9."""
    sections = [
        Section(
            number="1",
            title="Introdução",
            content=(
                f"Plano de Análise Estatística para o estudo: {request.study_title}\n"
                f"Patrocinador: {request.sponsor}\n"
                f"Fase: {request.phase}\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=["ICH E9", "RDC 9/2015"],
        ),
        Section(
            number="2",
            title="Objetivos e Desfechos",
            content=(
                "Desfecho primário: [INSERIR]\n"
                "Desfechos secundários:\n"
                + "\n".join(f"  - {ep}" for ep in request.endpoints)
                + f"\n\n{_PROVENANCE_NOTICE}"
            ),
            references=["ICH E9 Seção 2"],
        ),
        Section(
            number="3",
            title="Populações de Análise",
            content=(
                "ITT (Intenção de Tratar): todos os sujeitos randomizados.\n"
                "PP (Per Protocol): sujeitos sem desvios maiores.\n"
                "Segurança: todos os sujeitos que receberam pelo menos uma dose.\n\n"
                f"Critérios populacionais:\n{request.population_criteria}\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=["ICH E9 Seção 5"],
        ),
        Section(
            number="4",
            title="Métodos Estatísticos",
            content=(
                "Análise primária: [INSERIR método, nível de significância]\n"
                "Análise de sensibilidade: [INSERIR]\n"
                "Análise de subgrupos: [INSERIR]\n"
                "Tratamento de dados faltantes: [INSERIR]\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=["ICH E9 Seção 5.5"],
        ),
        Section(
            number="5",
            title="Tamanho Amostral",
            content=(
                "Justificativa: [INSERIR hipóteses, poder, alfa]\n"
                "Cálculo: [INSERIR fórmula ou simulação]\n"
                "Ajuste para perdas: [INSERIR]\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=["ICH E9 Seção 3.5"],
        ),
        Section(
            number="6",
            title="Análises Intermediárias",
            content=(
                "Análises interinas planejadas: [INSERIR ou N/A]\n"
                "Comitê de Monitoramento de Dados (DSMB): [INSERIR]\n"
                "Ajuste de multiplicidade: [INSERIR método]\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=["ICH E9 Seção 4.5", "RDC 9/2015 Art. 16"],
        ),
    ]

    return RegulatoryDocument(
        document_type=DocumentType.SAP,
        title=f"Plano de Análise Estatística — {request.study_title}",
        sections=sections,
        metadata=_metadata(request),
        generated_at=datetime.utcnow(),
        version="0.1-draft",
    )


def generate_icf_skeleton(request: RegulatoryRequest) -> RegulatoryDocument:
    """Gera esqueleto de TCLE conforme Res. CNS 466/2012 e Anvisa."""
    sections = [
        Section(
            number="1",
            title="Convite à Participação",
            content=(
                "Você está sendo convidado(a) a participar de uma pesquisa clínica. "
                "Este documento contém informações sobre o estudo para ajudá-lo(a) "
                "a decidir se deseja participar.\n\n"
                f"Título do estudo: {request.study_title}\n"
                f"Investigador principal: {request.principal_investigator}\n"
                f"Patrocinador: {request.sponsor}\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=["Res. CNS 466/2012 IV.3", "RDC 9/2015 Art. 10"],
        ),
        Section(
            number="2",
            title="Objetivo do Estudo",
            content=(
                f"Este estudo de fase {request.phase} investiga tratamentos na área de "
                f"{request.therapeutic_area}.\n"
                "[INSERIR explicação em linguagem acessível ao participante]\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=["Res. CNS 466/2012 IV.3.a"],
        ),
        Section(
            number="3",
            title="Procedimentos do Estudo",
            content=(
                "Se você concordar em participar, os seguintes procedimentos "
                "serão realizados:\n"
                "[INSERIR procedimentos em linguagem leiga]\n\n"
                "Duração da participação: [INSERIR]\n"
                "Número de visitas: [INSERIR]\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=["Res. CNS 466/2012 IV.3.b"],
        ),
        Section(
            number="4",
            title="Riscos e Desconfortos",
            content=(
                "Os possíveis riscos e desconfortos incluem:\n"
                "[INSERIR riscos conhecidos em linguagem acessível]\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=["Res. CNS 466/2012 IV.3.c"],
        ),
        Section(
            number="5",
            title="Benefícios",
            content=(
                "Os possíveis benefícios da sua participação incluem:\n"
                "[INSERIR benefícios diretos e indiretos]\n\n"
                "Nota: não há garantia de benefício individual.\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=["Res. CNS 466/2012 IV.3.d"],
        ),
        Section(
            number="6",
            title="Direitos do Participante",
            content=(
                "Sua participação é voluntária. Você pode:\n"
                "  - Recusar-se a participar sem penalidade\n"
                "  - Retirar seu consentimento a qualquer momento\n"
                "  - Solicitar informações atualizadas sobre o estudo\n"
                "  - Ter acesso aos resultados que lhe dizem respeito\n\n"
                "Em caso de dano decorrente da pesquisa, você tem direito à "
                "assistência integral e indenização conforme legislação vigente.\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=["Res. CNS 466/2012 IV.3.e-h", "RDC 9/2015 Art. 10 §2º"],
        ),
        Section(
            number="7",
            title="Confidencialidade",
            content=(
                "Seus dados pessoais serão mantidos em sigilo conforme a "
                "Lei Geral de Proteção de Dados (LGPD — Lei 13.709/2018). "
                "Apenas a equipe de pesquisa e autoridades regulatórias "
                "terão acesso aos seus dados identificados.\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=["Res. CNS 466/2012 IV.3.i", "LGPD Lei 13.709/2018"],
        ),
        Section(
            number="8",
            title="Contatos",
            content=(
                f"Investigador principal: {request.principal_investigator}\n"
                "Telefone: [INSERIR]\n"
                "E-mail: [INSERIR]\n\n"
                "Comitê de Ética em Pesquisa (CEP): [INSERIR dados do CEP]\n"
                "CONEP: (61) 3315-5877 — conep@saude.gov.br\n\n"
                f"{_PROVENANCE_NOTICE}"
            ),
            references=["Res. CNS 466/2012 IV.5"],
        ),
    ]

    return RegulatoryDocument(
        document_type=DocumentType.ICF,
        title=f"Termo de Consentimento Livre e Esclarecido — {request.study_title}",
        sections=sections,
        metadata=_metadata(request),
        generated_at=datetime.utcnow(),
        version="0.1-draft",
    )
