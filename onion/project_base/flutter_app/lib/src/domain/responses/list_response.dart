class ListResponse<T> {
  final List<T> data;
  final int total;
  final int page;
  final int pageSize;

  ListResponse({
    required this.data,
    required this.total,
    required this.page,
    required this.pageSize,
  });

  factory ListResponse.fromJson(
    Map<String, dynamic> json,
    T Function(Map<String, dynamic>) fromJsonT,
  ) {
    final items = (json['data'] as List<dynamic>?)
            ?.map((item) => fromJsonT(item as Map<String, dynamic>))
            .toList() ??
        [];

    return ListResponse(
      data: items,
      total: json['total'] as int? ?? items.length,
      page: json['page'] as int? ?? 1,
      pageSize: json['page_size'] as int? ?? items.length,
    );
  }
}