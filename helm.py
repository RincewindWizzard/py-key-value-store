import toml
import yaml
from loguru import logger
from types import SimpleNamespace
from pathlib import Path

HELMCHART_PATH = Path('helm')


def chart_yaml(ctx):
    return {
        'apiVersion': 'v2',
        'name': ctx.tool.poetry.name,
        'type': 'application',
        'version': ctx.tool.poetry.version,
        'appVersion': ctx.tool.poetry.version
    }


def deployment(ctx):
    return {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'metadata': {
            'name': ctx.tool.poetry.name,
            'labels': {
                'app': ctx.tool.poetry.name,
                'app.kubernetes.io/name': ctx.tool.poetry.name
            }
        },
        'spec': {
            'replicas': ctx.kubernetes.replicas,
            'selector': {
                'matchLabels': {
                    'app': ctx.tool.poetry.name
                }
            },
            'template': {
                'metadata': {
                    'labels': {
                        'app': ctx.tool.poetry.name,
                        'app.kubernetes.io/name': ctx.tool.poetry.name
                    }
                },
                'spec': {
                    'containers': [
                        {
                            'name': ctx.tool.poetry.name,
                            'image': f'{ctx.docker.repository}:{ctx.tool.poetry.version}',
                            'ports': [
                                {
                                    'containerPort': 8000
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }


def service(ctx):
    return {
        'apiVersion': 'v1',
        'kind': 'Service',
        'metadata': {
            'annotations': {
                'meta.helm.sh/release-name': ctx.tool.poetry.name,
                'meta.helm.sh/release-namespace': 'default'
            },
            'name': ctx.tool.poetry.name
        },
        'spec': {
            'ports': [
                {
                    'port': 80,
                    'protocol': 'TCP',
                    'targetPort': 8000
                }
            ],
            'selector': {
                'app.kubernetes.io/name': ctx.tool.poetry.name
            }
        }
    }


def ingress(ctx):
    return {
        'apiVersion': 'networking.k8s.io/v1',
        'kind': 'Ingress',
        'metadata': {
            'annotations': {
                'meta.helm.sh/release-name': ctx.tool.poetry.name,
                'meta.helm.sh/release-namespace': 'default',
                'nginx.ingress.kubernetes.io/rewrite-target': '/$2'
            },
            'name': 'ingress',
        },
        'spec': {
            'ingressClassName': 'nginx',
            'rules': [
                {
                    'http': {
                        'paths': [
                            {
                                'path': f'/{ctx.tool.poetry.name}(/|$)(.*)',
                                'pathType': 'Prefix',
                                'backend': {
                                    'service': {
                                        'name': ctx.tool.poetry.name,
                                        'port': {
                                            'number': 80
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }


def ingress_class(ctx):
    return {
        'apiVersion': 'networking.k8s.io/v1',
        'kind': 'IngressClass',
        'metadata': {
            'labels': {
                'app.kubernetes.io/component': 'controller'
            },
            'name': 'nginx',
            'annotations': {
                'ingressclass.kubernetes.io/is-default-class': 'true'
            }
        },
        'spec': {
            'controller': 'k8s.io/ingress-nginx'
        }
    }


def as_namespace(o):
    """
    Converts a recursive structure of dictionaries to a SimpleNamespace
    :param o:
    :return:
    """
    if isinstance(o, dict):
        return SimpleNamespace(**{k: as_namespace(v) for k, v in o.items()})
    else:
        return o


def main(*args, **kwargs):
    ctx = as_namespace(toml.load('./pyproject.toml'))
    # print(yaml.dump(toml.load('./pyproject.toml')))

    # exit(1)

    helmchart = {
        'Chart.yaml': chart_yaml,
        'templates/deployment.yaml': deployment,
        'templates/service.yaml': service,
        'templates/ingress.yaml': ingress,
        'templates/ingress_class.yaml': ingress_class,
        'values.yaml': lambda ctx: {}
    }

    logger.debug('Cleaning ./helm/')

    files = [file for file in HELMCHART_PATH.rglob('*') if file.is_file()]
    folders = [file for file in HELMCHART_PATH.rglob('*') if file.is_dir()]

    for path in files:
        logger.debug(f'remove {path}')
        path.unlink()

    for path in folders:
        logger.debug(f'remove {path}')
        path.rmdir()

    logger.debug('Creating ./helm/')

    for path, func in helmchart.items():
        path = HELMCHART_PATH / path
        path.parent.mkdir(parents=True, exist_ok=True)
        logger.debug(f'Creating {path}')
        with path.open('w') as f:
            f.write(yaml.dump(func(ctx)))


if __name__ == '__main__':
    main()
