# Ghi Âm Zalo PC 3.0.0

Phiên bản nâng cấp lớn chuyên biệt cho trải nghiệm làm việc thực tế, báo cáo cuộc gọi kinh doanh và giải quyết triệt để các giới hạn xử lý âm thanh AI:

1. **AI Xử lý cuộc gọi dài không giới hạn (Tự động nén thông minh chống lỗi 20MB)**:
   - Trước đây các cuộc gọi WAV hoặc gọi thoại/video dài trên 15 phút thường vượt ngưỡng 20MB và bị Gemini API từ chối.
   - Phiên bản 3.0.0 tích hợp thuật toán nén âm thanh giọng nói tự động (Mono 16kHz MP3 ~32kbps) độc quyền trước khi gửi dữ liệu lên Gemini API.
   - Dung lượng giảm hơn 97% trong khi độ trong trẻo và chi tiết giọng nói được bảo toàn tối đa. Nhờ đó, các cuộc gọi kéo dài 1–2 tiếng vẫn bóc băng và tóm tắt AI mượt mà 100%.
   - Tệp nén tạm thời được tự động dọn dẹp sạch sẽ ngay sau khi nhận phản hồi từ AI, bảo toàn nguyên trạng tệp âm thanh gốc của người dùng.

2. **Xuất biên bản cuộc gọi chuyên nghiệp (Call Minutes & Summary Export)**:
   - Bổ sung nút **"📄 Xuất biên bản"** trực tiếp trên thanh công cụ Thư viện và trong cửa sổ Chi tiết bản ghi.
   - Cho phép lưu biên bản cuộc gọi định dạng `.txt` hoặc `.doc` đầy đủ thông tin: Người liên hệ, ngày giờ, thời lượng, tóm tắt cốt lõi, danh sách việc cần làm (Action Items), đánh giá thái độ, mốc thời gian và toàn văn bóc băng.
   - Tự động gợi ý mở tệp ngay sau khi lưu để kiểm tra hoặc gửi cho đối tác/khách hàng.

3. **Sao chép nhanh 1-Click (1-Click Copy to Clipboard)**:
   - Nút **"📋 Sao chép tóm tắt"**: Sao chép nội dung tóm tắt và việc cần làm kèm tiêu đề chuẩn hóa để dán (Ctrl+V) tức thì vào khung chat Zalo, Messenger hoặc Email.
   - Nút **"📋 Sao chép bóc băng"**: Sao chép toàn bộ văn bản phiên âm từng câu.

4. **Tìm kiếm toàn văn thông minh trong Thư viện (Full-Text Transcript & Note Search)**:
   - Khung tìm kiếm trong Thư viện giờ đây hỗ trợ tìm kiếm sâu đa tầng: Quét tên bản ghi, tên người gọi/liên hệ, ghi chú riêng, nội dung tóm tắt AI, danh sách việc cần làm và toàn văn bóc băng.
   - Hỗ trợ tìm kiếm tiếng Việt không dấu (ví dụ: gõ `hop dong`, `chiet khau`, `thu hai` sẽ tìm thấy các cuộc gọi thảo luận về các chủ đề tương ứng).

5. **Hiển thị Tên người gọi & Nhận diện nâng cao (Caller Contact Name)**:
   - Tự động bóc tách và làm nổi bật thông tin Người liên hệ trong bản mô tả chi tiết phiên ghi âm và trong biên bản xuất bản ghi.
   - Hỗ trợ nhận diện tên người gọi trực tiếp từ tiến trình gọi chuyên biệt `ZaloCall.exe`.

6. **Xóa bản ghi an toàn trực tiếp từ Thư viện (Delete Recording)**:
   - Bổ sung nút **"🗑 Xóa"** trên thanh công cụ và phím tắt `Delete`.
   - Có hộp thoại xác nhận an toàn, tự động dừng phát và dọn sạch cả tệp âm thanh lẫn tệp dữ liệu kèm theo (`.json`).

7. **Tự động Fallback thiết bị âm thanh (Chống mất cuộc gọi)**:
   - Khi tai nghe Bluetooth hoặc USB bị rút/ngắt kết nối, phần mềm tự động chuyển sang Thiết bị Mặc định của Windows (Default Device) để ghi âm, không làm mất trắng cuộc gọi quan trọng.

8. **Lọc thông minh cuộc gọi rác / cuộc gọi nhỡ (< 5s)**:
   - Ở chế độ Tự Ghi, các cuộc gọi nhỡ, nháy máy hoặc từ chối kết thúc dưới 5 giây sẽ tự động được dọn dẹp, không làm rác thư viện bản ghi.

9. **Thanh nổi Mini có nút Đánh dấu mốc nhanh (`🚩 Mốc`)**:
   - Cho phép người dùng lưu lại mốc giây quan trọng (giá cả, địa chỉ, lịch hẹn) ngay trong khi đang gọi điện mà không cần mở to cửa sổ chính.

10. **Tương thích Gemini AI Model & Báo lỗi thông minh**:
    - Tự động luân chuyển model AI chính thức (`gemini-2.5-flash`, `gemini-1.5-flash`, `gemini-2.0-flash`).
    - Cảnh báo rõ ràng và cung cấp liên kết lấy key miễn phí khi API Key không hợp lệ.

11. **Cắt đoạn âm thanh đa luồng & Huy hiệu AI**:
    - Cắt âm thanh chạy ngầm (không đơ cửa sổ), tự động kế thừa tên người gọi và ngày giờ từ bản ghi gốc.
    - Hiển thị biểu tượng `🤖` trong danh sách để người dùng nhận biết ngay bản ghi nào đã có AI tóm tắt/bóc băng.
