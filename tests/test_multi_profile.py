#!/usr/bin/env python3
"""
OPB Sistema - Test Suite para Sistema Multi-Perfil
Testes unitários e de integração para profile_manager.py e endpoints de perfil
"""

import os
import sys
import json
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Adicionar o diretório do projeto ao path
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from profile_manager import (
    get_active_profile,
    set_active_profile,
    list_profiles,
    get_profile_config,
    get_profile_path,
    get_acervo_path,
    get_cerebro_path,
    get_output_path,
    get_perfil_path,
    PERFIS_CONFIG,
    PERFIS_PATH
)


# ============================================
# FIXTURES
# ============================================

@pytest.fixture
def temp_perfis_dir():
    """Cria um diretório temporário para testes de perfis."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Criar estrutura de perfis de teste
        perfis_config = {
            "ativo": "perfil-teste-1",
            "perfis": [
                {
                    "id": "perfil-teste-1",
                    "nome": "Perfil Teste 1",
                    "icone": "🧪",
                    "descricao": "Perfil para testes unitários"
                },
                {
                    "id": "perfil-teste-2",
                    "nome": "Perfil Teste 2",
                    "icone": "🔬",
                    "descricao": "Segundo perfil para testes"
                }
            ]
        }
        
        # Salvar perfis.json
        (tmp_path / "perfis.json").write_text(
            json.dumps(perfis_config, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        
        # Criar estrutura de diretórios para cada perfil
        for perfil in perfis_config["perfis"]:
            perfil_id = perfil["id"]
            base = tmp_path / perfil_id
            (base / "perfil").mkdir(parents=True)
            (base / "cerebro").mkdir(parents=True)
            (base / "acervo").mkdir(parents=True)
            (base / "output").mkdir(parents=True)
            
            # Criar config.json para cada perfil
            config = {
                "nome": perfil["nome"],
                "icone": perfil["icone"],
                "descricao": perfil["descricao"],
                "configuracoes": {
                    "tema": "dark",
                    "idioma": "pt-BR"
                }
            }
            (base / "perfil" / "config.json").write_text(
                json.dumps(config, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
        
        # Patch das constantes do module
        with patch('profile_manager.PERFIS_PATH', tmp_path), \
             patch('profile_manager.PERFIS_CONFIG', tmp_path / "perfis.json"):
            yield tmp_path


# ============================================
# TESTES UNITÁRIOS - profile_manager.py
# ============================================

class TestGetActiveProfile:
    """Testes para get_active_profile()."""
    
    def test_retorna_perfil_ativo_do_config(self, temp_perfis_dir):
        """Deve retornar o perfil ativo definido em perfis.json."""
        ativo = get_active_profile()
        assert ativo == "perfil-teste-1"
    
    def test_retorna_padrao_se_config_nao_existe(self):
        """Deve retornar 'paz-na-conta' se perfis.json não existir."""
        with patch('profile_manager.PERFIS_CONFIG', Path("/nonexistent/perfis.json")):
            ativo = get_active_profile()
            assert ativo == "paz-na-conta"
    
    def test_retorna_padrao_se_config_invalido(self, temp_perfis_dir):
        """Deve retornar padrão se o config estiver corrompido."""
        with patch('profile_manager.PERFIS_CONFIG') as mock_config:
            mock_config.exists.return_value = True
            mock_config.read_text.side_effect = json.JSONDecodeError("test", "doc", 0)
            ativo = get_active_profile()
            assert ativo == "paz-na-conta"


class TestSetActiveProfile:
    """Testes para set_active_profile()."""
    
    def test_define_perfil_ativo_com_sucesso(self, temp_perfis_dir):
        """Deve definir o perfil ativo com sucesso."""
        result = set_active_profile("perfil-teste-2")
        assert result["success"] is True
        assert result["profile_id"] == "perfil-teste-2"
        
        # Verificar que o arquivo foi atualizado
        ativo = get_active_profile()
        assert ativo == "perfil-teste-2"
    
    def test_falha_perfil_inexistente(self, temp_perfis_dir):
        """Deve falhar ao tentar definir um perfil que não existe."""
        result = set_active_profile("perfil-inexistente")
        assert result["success"] is False
        assert "não existe" in result["error"]
    
    def test_falha_config_nao_existe(self):
        """Deve falhar se perfis.json não existir."""
        with patch('profile_manager.PERFIS_CONFIG', Path("/nonexistent/perfis.json")):
            result = set_active_profile("qualquer")
            assert result["success"] is False
            assert "not found" in result["error"]


class TestListProfiles:
    """Testes para list_profiles()."""
    
    def test_lista_todos_perfis(self, temp_perfis_dir):
        """Deve listar todos os perfis disponíveis."""
        perfis = list_profiles()
        assert len(perfis) == 2
        assert perfis[0]["id"] == "perfil-teste-1"
        assert perfis[1]["id"] == "perfil-teste-2"
    
    def test_lista_vazia_se_config_nao_existe(self):
        """Deve retornar lista vazia se config não existir."""
        with patch('profile_manager.PERFIS_CONFIG', Path("/nonexistent/perfis.json")):
            perfis = list_profiles()
            assert perfis == []
    
    def test_lista_vazia_se_config_invalido(self, temp_perfis_dir):
        """Deve retornar lista vazia se config estiver corrompido."""
        with patch('profile_manager.PERFIS_CONFIG') as mock_config:
            mock_config.exists.return_value = True
            mock_config.read_text.side_effect = Exception("test error")
            perfis = list_profiles()
            assert perfis == []


class TestGetProfileConfig:
    """Testes para get_profile_config()."""
    
    def test_retorna_config_do_perfil(self, temp_perfis_dir):
        """Deve retornar a configuração do perfil."""
        config = get_profile_config("perfil-teste-1")
        assert config is not None
        assert config["nome"] == "Perfil Teste 1"
        assert config["icone"] == "🧪"
    
    def test_retorna_none_se_perfil_nao_existe(self, temp_perfis_dir):
        """Deve retornar None se o perfil não existir."""
        config = get_profile_config("perfil-inexistente")
        assert config is None
    
    def test_usa_perfil_ativo_se_none(self, temp_perfis_dir):
        """Deve usar o perfil ativo se nenhum for especificado."""
        config = get_profile_config()
        assert config is not None
        assert config["nome"] == "Perfil Teste 1"


class TestGetProfilePath:
    """Testes para funções de path."""
    
    def test_get_profile_path_base(self, temp_perfis_dir):
        """Deve retornar o path base do perfil."""
        path = get_profile_path("perfil-teste-1")
        assert str(path).endswith("perfil-teste-1")
    
    def test_get_profile_path_com_subdir(self, temp_perfis_dir):
        """Deve retornar o path com subdiretório."""
        path = get_profile_path("perfil-teste-1", "cerebro")
        assert "perfil-teste-1" in str(path)
        assert "cerebro" in str(path)
    
    def test_get_acervo_path(self, temp_perfis_dir):
        """Deve retornar o path do acervo."""
        path = get_acervo_path("perfil-teste-1")
        assert "perfil-teste-1" in str(path)
        assert "acervo" in str(path)
    
    def test_get_cerebro_path(self, temp_perfis_dir):
        """Deve retornar o path do cerebro."""
        path = get_cerebro_path("perfil-teste-1")
        assert "perfil-teste-1" in str(path)
        assert "cerebro" in str(path)
    
    def test_get_output_path(self, temp_perfis_dir):
        """Deve retornar o path do output."""
        path = get_output_path("perfil-teste-1")
        assert "perfil-teste-1" in str(path)
        assert "output" in str(path)
    
    def test_get_perfil_path(self, temp_perfis_dir):
        """Deve retornar o path do perfil."""
        path = get_perfil_path("perfil-teste-1")
        assert "perfil-teste-1" in str(path)
        assert "perfil" in str(path)


# ============================================
# TESTES DE ISOLAMENTO DE PERFIS
# ============================================

class TestProfileIsolation:
    """Testes para garantir isolamento entre perfis."""
    
    def test_dados_nao_compartilhados_entre_perfis(self, temp_perfis_dir):
        """Dados de um perfil não devem aparecer em outro."""
        # Criar dados no perfil 1
        perfil1_acervo = get_acervo_path("perfil-teste-1")
        (perfil1_acervo / "teste.md").write_text("Dados do perfil 1", encoding='utf-8')
        
        # Verificar que perfil 2 não tem esses dados
        perfil2_acervo = get_acervo_path("perfil-teste-2")
        assert not (perfil2_acervo / "teste.md").exists()
    
    def test_cada_perfil_tem_seu_cerebro(self, temp_perfis_dir):
        """Cada perfil deve ter seu próprio cerebro."""
        cerebro1 = get_cerebro_path("perfil-teste-1")
        cerebro2 = get_cerebro_path("perfil-teste-2")
        
        # Criar arquivo no cerebro 1
        (cerebro1 / "dados1.json").write_text('{"perfil": 1}', encoding='utf-8')
        
        # Verificar que cerebro 2 não tem o arquivo
        assert not (cerebro2 / "dados1.json").exists()
    
    def test_output_isolado_por_perfil(self, temp_perfis_dir):
        """Output de cada perfil deve ser isolado."""
        output1 = get_output_path("perfil-teste-1")
        output2 = get_output_path("perfil-teste-2")
        
        # Criar arquivo no output 1
        (output1 / "relatorio.md").write_text("Relatório do perfil 1", encoding='utf-8')
        
        # Verificar que output 2 não tem o arquivo
        assert not (output2 / "relatorio.md").exists()


# ============================================
# TESTES DE INTEGRAÇÃO - API ENDPOINTS
# ============================================

class TestProfileAPIEndpoints:
    """Testes para endpoints de perfil da API."""
    
    @pytest.fixture
    def client(self):
        """Cria um cliente de teste para a API."""
        # Importar o app diretamente (sem patching problemático)
        from api_server import app
        app.config['TESTING'] = True
        
        with app.test_client() as client:
            yield client
    
    def test_get_perfis_lista_todos(self, client):
        """GET /api/perfis deve listar todos os perfis."""
        response = client.get('/api/perfis')
        assert response.status_code == 200
        
        data = response.get_json()
        assert "perfis" in data
        assert "ativo" in data
        assert "total" in data
        assert data["total"] >= 2  # Deve ter pelo menos 2 perfis
    
    def test_get_perfil_ativo(self, client):
        """GET /api/perfis/ativo deve retornar o perfil ativo."""
        response = client.get('/api/perfis/ativo')
        assert response.status_code == 200
        
        data = response.get_json()
        assert "id" in data
        assert "config" in data
    
    def test_post_perfil_ativo_sucesso(self, client):
        """POST /api/perfis/ativo deve trocar o perfil ativo."""
        # Usar um perfil que existe (verificar primeiro)
        list_response = client.get('/api/perfis')
        perfis = list_response.get_json()["perfis"]
        perfil_id = perfis[1]["id"] if len(perfis) > 1 else perfis[0]["id"]
        
        response = client.post('/api/perfis/ativo', json={
            "perfil_id": perfil_id
        })
        assert response.status_code == 200
        
        data = response.get_json()
        assert data["success"] is True
        assert data["perfil_id"] == perfil_id
    
    def test_post_perfil_ativo_falha_sem_id(self, client):
        """POST /api/perfis/ativo deve falhar sem perfil_id."""
        response = client.post('/api/perfis/ativo', json={})
        assert response.status_code == 400
        
        data = response.get_json()
        assert "error" in data
    
    def test_post_perfil_ativo_falha_perfil_inexistente(self, client):
        """POST /api/perfis/ativo deve falhar com perfil inexistente."""
        response = client.post('/api/perfis/ativo', json={
            "perfil_id": "perfil-inexistente-123"
        })
        assert response.status_code == 400
        
        data = response.get_json()
        assert "success" in data or "error" in data
    
    def test_get_perfil_config(self, client):
        """GET /api/perfis/<id>/config deve retornar config do perfil."""
        # Usar um perfil que existe
        list_response = client.get('/api/perfis')
        perfis = list_response.get_json()["perfis"]
        perfil_id = perfis[0]["id"]
        
        response = client.get(f'/api/perfis/{perfil_id}/config')
        assert response.status_code == 200
        
        data = response.get_json()
        assert "nome" in data
    
    def test_get_perfil_config_nao_existe(self, client):
        """GET /api/perfis/<id>/config deve falhar para perfil inexistente."""
        response = client.get('/api/perfis/perfil-inexistente-123/config')
        assert response.status_code == 404


# ============================================
# TESTES DE EDGE CASES
# ============================================

class TestEdgeCases:
    """Testes para casos extremos."""
    
    def test_perfis_config_corrompido(self, temp_perfis_dir):
        """Deve lidar com perfis.json corrompido."""
        with patch('profile_manager.PERFIS_CONFIG') as mock_config:
            mock_config.exists.return_value = True
            mock_config.read_text.side_effect = json.JSONDecodeError("test", "doc", 0)
            
            # get_active_profile deve retornar padrão
            assert get_active_profile() == "paz-na-conta"
            
            # list_profiles deve retornar lista vazia
            assert list_profiles() == []
    
    def test_perfil_sem_config_json(self, temp_perfis_dir):
        """Deve lidar com perfil que não tem config.json."""
        # Remover config.json de um perfil
        config_path = temp_perfis_dir / "perfil-teste-2" / "perfil" / "config.json"
        if config_path.exists():
            config_path.unlink()
        
        config = get_profile_config("perfil-teste-2")
        assert config is None
    
    def test_troca_multipla_de_perfis(self, temp_perfis_dir):
        """Deve permitir trocar de perfil múltiplas vezes."""
        perfis = ["perfil-teste-1", "perfil-teste-2", "perfil-teste-1", "perfil-teste-2"]
        
        for perfil_id in perfis:
            result = set_active_profile(perfil_id)
            assert result["success"] is True
            assert get_active_profile() == perfil_id
    
    def test_perfis_com_caracteres_especiais(self, temp_perfis_dir):
        """Deve lidar com nomes de perfil com caracteres especiais."""
        # Este teste verifica se o sistema handle UTF-8 corretamente
        config = get_profile_config("perfil-teste-1")
        assert config is not None
        assert "🧪" in config.get("icone", "")


# ============================================
# RUNNER
# ============================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
