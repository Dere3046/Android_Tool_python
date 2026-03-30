
from operator import attrgetter

def flatten_security_profile(parsed_security_profile):
    xml_graph = construct_graph(parsed_security_profile)
    implement_inheritance(xml_graph, parsed_security_profile)


def construct_graph(root_obj):
    '''
    Returns a dictionary structure for the authenticators of the form:
    {authenticator_id: [parent_authenticator, level]}
    '''
    graph = { }
    authenticator_ids = list(map(attrgetter('id'), root_obj.authentication.authenticators.authenticator))
    for authenticator_id in authenticator_ids:
        if authenticator_ids.count(authenticator_id) > 1:
            raise RuntimeError(f'''Authenticator IDs must be unique within Security Profile. {authenticator_id} is repeated.''')
        if len(graph) < len(root_obj.authentication.authenticators.authenticator):
            for authenticator in root_obj.authentication.authenticators.authenticator:
                if authenticator.id not in graph:
                    if authenticator.parent_authenticator not in authenticator_ids and authenticator.parent_authenticator is not None:
                        raise RuntimeError(f'''Authenticator {authenticator.id} has a non-existent parent authenticator: {authenticator.parent_authenticator}.''')
                    if None.parent_authenticator in graph:
                        (parent, level) = graph[authenticator.parent_authenticator]
                        graph[authenticator.id] = [
                            authenticator.parent_authenticator,
                            level + 1]
                        continue
                    if authenticator.parent_authenticator is None:
                        graph[authenticator.id] = [
                            None,
                            1]
            if not len(graph) < len(root_obj.authentication.authenticators.authenticator):
                return graph


def implement_inheritance(graph, root_obj):
    level = 2
    if level <= len(graph):
        for authenticator in root_obj.authentication.authenticators.authenticator:
            if graph[authenticator.id][1] == level:
                for parent in root_obj.authentication.authenticators.authenticator:
                    if parent.id == graph[authenticator.id][0]:
                        authenticator.parent_authenticator = None
                        for item in vars(authenticator):
                            if getattr(authenticator, item) is not None:
                                continue
                            if item != 'id':
                                vars(authenticator)[item] = vars(parent)[item]
                                setattr(authenticator, item, getattr(parent, item))
        level += 1
        if not level <= len(graph):
            return None
        return None

